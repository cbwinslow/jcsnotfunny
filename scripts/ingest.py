"""Simple ingest helper (stub)

- Scan `raw_videos/<episode>`
- Verify checksums
- Create proxies in `working_projects/<episode>/proxies/`
- Write metadata JSON
"""

import os
import json

def ingest_episode(episode_dir):
    # TODO: implement real ingest
    files = [f for f in os.listdir(episode_dir) if not f.startswith('.')]
    meta = {'files': files}
    with open(os.path.join(episode_dir,'ingest_meta.json'),'w') as fh:
        json.dump(meta, fh)

if __name__ == '__main__':
    print('Run with: python scripts/ingest.py <episode_dir>')
