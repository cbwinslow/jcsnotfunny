#!/usr/bin/env python3
"""Package agents and toolsets into an archive for distribution or inspection."""

from pathlib import Path
import tarfile

ROOT = Path(__file__).parent.parent
AGENTS_DIR = ROOT / 'agents'
BUILD_DIR = ROOT / 'build'
BUILD_DIR.mkdir(exist_ok=True)

archive_path = BUILD_DIR / 'agents.tar.gz'
with tarfile.open(archive_path, 'w:gz') as tf:
    tf.add(AGENTS_DIR, arcname='agents')

print(f'Packaged agents to {archive_path}')
