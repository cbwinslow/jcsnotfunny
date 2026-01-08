"""Score text or transcript segments for humor using a fine-tuned model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from scripts.clip_generator import parse_transcript


def load_segments(input_path: str) -> List[Dict]:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")
    suffix = path.suffix.lower()
    if suffix in {".vtt", ".srt", ".json"}:
        return parse_transcript(str(path))
    if suffix == ".jsonl":
        segments = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if not isinstance(data, dict):
                continue
            text = (data.get("text") or "").strip()
            if not text:
                continue
            segments.append({"text": text, "start": data.get("start"), "end": data.get("end")})
        return segments
    if suffix == ".txt":
        return [{"text": line.strip()} for line in path.read_text().splitlines() if line.strip()]
    raise ValueError(f"Unsupported input format: {suffix}")


def score_segments(model_dir: str, segments: List[Dict], batch_size: int) -> List[Dict]:
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
    except ImportError as exc:
        raise RuntimeError("transformers and torch are required for scoring") from exc

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    scored = []
    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        texts = [seg.get("text", "") for seg in batch]
        inputs = tokenizer(texts, truncation=True, padding=True, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[:, 1].detach().cpu().numpy().tolist()
        for seg, score in zip(batch, probs):
            entry = dict(seg)
            entry["humor_score"] = float(score)
            scored.append(entry)
    return scored


def main() -> None:
    parser = argparse.ArgumentParser(description="Score humor for transcript segments")
    parser.add_argument("--model_dir", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    segments = load_segments(args.input)
    scored = score_segments(args.model_dir, segments, args.batch_size)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"segments": scored}, indent=2))
    print(f"Wrote humor scores to {output_path}")


if __name__ == "__main__":
    main()
