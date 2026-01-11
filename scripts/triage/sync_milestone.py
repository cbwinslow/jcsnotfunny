#!/usr/bin/env python3
"""Utility to attach a list of issue numbers to a milestone and add a brief comment.

Usage:
  python scripts/triage/sync_milestone.py --milestone 5 21 24 25 26 27 28

Requires: `gh` CLI authenticated with repo access.
"""
import argparse
import subprocess
import sys


def run(cmd):
    print('> ', ' '.join(cmd))
    subprocess.check_call(cmd)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--milestone', type=int, required=True)
    p.add_argument('issues', nargs='+', type=int)
    args = p.parse_args()

    for n in args.issues:
        print(f'Attaching issue {n} to milestone {args.milestone}')
        run(['gh', 'api', '-X', 'PATCH', f'repos/cbwinslow/jcsnotfunny/issues/{n}', '-f', f'milestone={args.milestone}'])
        run(['gh', 'issue', 'comment', str(n), '--repo', 'cbwinslow/jcsnotfunny', '-b', f'Automated: Attached to milestone #{args.milestone} for Transcription & Captioning.'])

    print('Done')
