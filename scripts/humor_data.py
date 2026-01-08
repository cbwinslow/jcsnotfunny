"""Utilities for loading and normalizing humor training data."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


LABEL_TRUE = {"1", "true", "yes", "y", "funny", "humor", "humorous", "laugh"}
LABEL_FALSE = {"0", "false", "no", "n", "not_funny", "serious"}


def normalize_label(value) -> int:
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, (int, float)):
        return 1 if int(value) != 0 else 0
    if value is None:
        raise ValueError("Label is required")
    text = str(value).strip().lower()
    if text in LABEL_TRUE:
        return 1
    if text in LABEL_FALSE:
        return 0
    if text.isdigit():
        return 1 if int(text) != 0 else 0
    raise ValueError(f"Unsupported label value: {value}")


def _normalize_text(value: str) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_example(row: Dict) -> Dict:
    text = _normalize_text(row.get("text") or row.get("transcript") or row.get("utterance"))
    if not text:
        return {}
    label = normalize_label(row.get("label") or row.get("is_funny"))
    normalized = {
        "text": text,
        "label": label,
        "source_id": row.get("source_id") or row.get("clip_id") or "",
        "start": row.get("start") or row.get("start_time"),
        "end": row.get("end") or row.get("end_time"),
        "notes": row.get("notes") or "",
    }
    return normalized


def _load_csv(path: Path) -> List[Dict]:
    examples: List[Dict] = []
    with path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            normalized = _normalize_example(row)
            if normalized:
                examples.append(normalized)
    return examples


def _load_json(path: Path) -> List[Dict]:
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        records = data.get("examples") or data.get("data") or []
    elif isinstance(data, list):
        records = data
    else:
        records = []
    examples = []
    for row in records:
        if not isinstance(row, dict):
            continue
        normalized = _normalize_example(row)
        if normalized:
            examples.append(normalized)
    return examples


def _load_jsonl(path: Path) -> List[Dict]:
    examples: List[Dict] = []
    with path.open("r") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                continue
            normalized = _normalize_example(row)
            if normalized:
                examples.append(normalized)
    return examples


def load_local_examples(path: str) -> List[Dict]:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")
    suffix = source.suffix.lower()
    if suffix == ".csv":
        return _load_csv(source)
    if suffix == ".jsonl":
        return _load_jsonl(source)
    if suffix == ".json":
        return _load_json(source)
    raise ValueError(f"Unsupported dataset format: {suffix}")


def split_examples(examples: List[Dict], validation_ratio: float, seed: int) -> Tuple[List[Dict], List[Dict]]:
    if not examples:
        return [], []
    ratio = max(0.0, min(validation_ratio, 0.5))
    if ratio == 0:
        return examples, []
    rng = __import__("random")
    rng.seed(seed)
    shuffled = examples[:]
    rng.shuffle(shuffled)
    cutoff = max(1, int(len(shuffled) * (1.0 - ratio)))
    return shuffled[:cutoff], shuffled[cutoff:]


def summarize_labels(examples: Iterable[Dict]) -> Dict[str, int]:
    counts = {"funny": 0, "not_funny": 0}
    for row in examples:
        label = row.get("label", 0)
        if label:
            counts["funny"] += 1
        else:
            counts["not_funny"] += 1
    return counts
