"""Compute simple diarization metrics between expected and actual diarization JSON files.

Usage:
  python scripts/transcribe_agent/compute_diar_metrics.py --expected expected.diar.json --actual actual.diar.json --output metrics.json

Metrics produced:
- avg_boundary_error_seconds
- expected_segments
- actual_segments
- coverage (ratio of speech time covered by actual segments over expected speech time)
"""
import argparse
import json
from typing import List


def load_diar(path: str) -> List[dict]:
    with open(path, 'r') as fh:
        return json.load(fh)


def avg_boundary_error(expected: List[dict], actual: List[dict]) -> float:
    # assumes segments are ordered and same count for simplicity
    if not expected or not actual:
        return float('inf')
    n = min(len(expected), len(actual))
    total = 0.0
    count = 0
    for i in range(n):
        e = expected[i]
        a = actual[i]
        total += abs(e['start'] - a['start'])
        total += abs(e['end'] - a['end'])
        count += 2
    return total / count if count else float('inf')


def speech_coverage(expected: List[dict], actual: List[dict]) -> float:
    # compute total expected speech duration and total overlap with actual segments
    def total_duration(segs):
        return sum(s['end'] - s['start'] for s in segs)

    def overlap(a, b):
        return max(0.0, min(a['end'], b['end']) - max(a['start'], b['start']))

    exp_total = total_duration(expected)
    if exp_total == 0:
        return 0.0
    overlap_total = 0.0
    for e in expected:
        for a in actual:
            overlap_total += overlap(e, a)
    return min(1.0, overlap_total / exp_total)


def compute(expected_path: str, actual_path: str) -> dict:
    expected = load_diar(expected_path)
    actual = load_diar(actual_path)
    return {
        'avg_boundary_error_seconds': avg_boundary_error(expected, actual),
        'expected_segments': len(expected),
        'actual_segments': len(actual),
        'coverage': speech_coverage(expected, actual),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--expected', required=True)
    p.add_argument('--actual', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()

    metrics = compute(args.expected, args.actual)
    with open(args.output, 'w') as fh:
        json.dump(metrics, fh, indent=2)
    print('Metrics written to', args.output)


if __name__ == '__main__':
    main()
