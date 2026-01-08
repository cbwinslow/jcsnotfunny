"""Fine-tune a humor classifier with optional LoRA for local GPU training."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

from scripts.humor_data import load_local_examples, split_examples, summarize_labels, normalize_label


def load_hf_examples(dataset_name: str, split: str, text_field: str, label_field: str) -> List[Dict]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("datasets is required for Hugging Face datasets") from exc

    dataset = load_dataset(dataset_name, split=split)
    examples = []
    for row in dataset:
        text = row.get(text_field) or row.get("text")
        label = row.get(label_field) if label_field else row.get("label")
        if text is None or label is None:
            continue
        examples.append({"text": str(text).strip(), "label": normalize_label(label)})
    return examples


def build_dataset(local_path: str | None, hf_name: str | None, hf_split: str, text_field: str, label_field: str) -> List[Dict]:
    examples: List[Dict] = []
    if local_path:
        examples.extend(load_local_examples(local_path))
    if hf_name:
        examples.extend(load_hf_examples(hf_name, hf_split, text_field, label_field))
    if not examples:
        raise ValueError("No training data found. Provide --local_dataset or --hf_dataset.")
    return examples


def train(args: argparse.Namespace) -> Dict:
    try:
        import torch
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification,
            DataCollatorWithPadding,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise RuntimeError("transformers and torch are required for training") from exc

    try:
        from datasets import Dataset
    except ImportError as exc:
        raise RuntimeError("datasets is required for training") from exc

    examples = build_dataset(
        args.local_dataset,
        args.hf_dataset,
        args.hf_split,
        args.text_field,
        args.label_field,
    )
    train_examples, val_examples = split_examples(examples, args.validation_ratio, args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=args.max_length)

    train_dataset = Dataset.from_list(train_examples).map(tokenize, batched=True)
    eval_dataset = Dataset.from_list(val_examples).map(tokenize, batched=True) if val_examples else None

    model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=2)

    use_lora = not args.full_finetune
    if use_lora:
        try:
            from peft import LoraConfig, TaskType, get_peft_model
        except ImportError as exc:
            raise RuntimeError("peft is required for LoRA fine-tuning") from exc
        target_modules = args.lora_target_modules.split(",") if args.lora_target_modules else ["query", "value"]
        lora_config = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=args.lora_r,
            lora_alpha=args.lora_alpha,
            lora_dropout=args.lora_dropout,
            target_modules=target_modules,
        )
        model = get_peft_model(model, lora_config)

    def compute_metrics(eval_pred):
        import numpy as np
        from sklearn.metrics import accuracy_score, f1_score

        logits, labels = eval_pred
        preds = np.argmax(logits, axis=1)
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds),
        }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        logging_steps=25,
        evaluation_strategy="steps" if eval_dataset is not None else "no",
        eval_steps=100 if eval_dataset is not None else None,
        save_steps=100,
        save_total_limit=2,
        load_best_model_at_end=bool(eval_dataset is not None),
        metric_for_best_model="f1",
        seed=args.seed,
        fp16=torch.cuda.is_available(),
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics if eval_dataset is not None else None,
    )

    trainer.train()
    metrics = trainer.evaluate() if eval_dataset is not None else {}

    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    summary = {
        "model_name": args.model_name,
        "output_dir": str(output_dir),
        "train_counts": summarize_labels(train_examples),
        "eval_counts": summarize_labels(val_examples),
        "metrics": metrics,
        "use_lora": use_lora,
    }
    (output_dir / "training_summary.json").write_text(json.dumps(summary, indent=2))
    (output_dir / "label_map.json").write_text(json.dumps({"not_funny": 0, "funny": 1}, indent=2))
    (output_dir / "training_config.json").write_text(json.dumps(vars(args), indent=2))
    (output_dir / "humor_model_card.md").write_text(
        "# Humor Classifier\n\n"
        f"- Base model: {args.model_name}\n"
        f"- Training examples: {len(train_examples)}\n"
        f"- Validation examples: {len(val_examples)}\n"
        f"- LoRA: {use_lora}\n"
    )

    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fine-tune a humor classifier")
    parser.add_argument("--config", default=None, help="Path to JSON config file")
    parser.add_argument("--model_name", default="distilroberta-base")
    parser.add_argument("--output_dir", default="models/humor_classifier")
    parser.add_argument("--local_dataset", default=None)
    parser.add_argument("--hf_dataset", default=None)
    parser.add_argument("--hf_split", default="train")
    parser.add_argument("--text_field", default="text")
    parser.add_argument("--label_field", default="label")
    parser.add_argument("--validation_ratio", type=float, default=0.1)
    parser.add_argument("--max_length", type=int, default=256)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--eval_batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--warmup_ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--full_finetune", action="store_true", default=False)
    parser.add_argument("--lora_r", type=int, default=8)
    parser.add_argument("--lora_alpha", type=int, default=16)
    parser.add_argument("--lora_dropout", type=float, default=0.05)
    parser.add_argument("--lora_target_modules", default="query,value")
    return parser


def parse_args() -> argparse.Namespace:
    parser = build_parser()
    pre_args, _ = parser.parse_known_args()
    if pre_args.config:
        config_path = Path(pre_args.config)
        if not config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        config = json.loads(config_path.read_text())
        allowed = {action.dest for action in parser._actions}
        defaults = {k: v for k, v in config.items() if k in allowed}
        parser.set_defaults(**defaults)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = train(args)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
