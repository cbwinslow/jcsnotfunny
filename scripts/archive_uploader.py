"""Archive uploader utilities for local manifests and S3-compatible storage."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from scripts.social_workflows import load_dotenv


@dataclass
class ArchiveItem:
    path: str
    size_bytes: int
    sha256: Optional[str] = None

    def as_dict(self) -> Dict:
        return {
            'path': self.path,
            'size_bytes': self.size_bytes,
            'sha256': self.sha256,
        }


def _hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_manifest(paths: Iterable[str], hash_files: bool = False) -> List[ArchiveItem]:
    items: List[ArchiveItem] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for item in path.rglob('*'):
                if item.is_file():
                    items.append(_build_item(item, hash_files))
        elif path.is_file():
            items.append(_build_item(path, hash_files))
    return items


def _build_item(path: Path, hash_files: bool) -> ArchiveItem:
    sha = _hash_file(path) if hash_files else None
    return ArchiveItem(path=str(path), size_bytes=path.stat().st_size, sha256=sha)


def write_manifest(items: List[ArchiveItem], out_path: str) -> str:
    payload = [item.as_dict() for item in items]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as fh:
        json.dump(payload, fh, indent=2)
    return out_path


def upload_manifest_s3(
    items: List[ArchiveItem],
    bucket: str,
    endpoint: str,
    access_key: str,
    secret_key: str,
    prefix: str = '',
) -> Dict:
    try:
        import boto3  # type: ignore
    except Exception as exc:
        raise RuntimeError('boto3 not installed; cannot upload') from exc
    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    client = session.client('s3', endpoint_url=endpoint)
    uploaded = []
    for item in items:
        key = f"{prefix}{Path(item.path).name}"
        client.upload_file(item.path, bucket, key)
        uploaded.append({'path': item.path, 'key': key})
    return {'bucket': bucket, 'uploaded': uploaded}


def main() -> None:
    parser = argparse.ArgumentParser(description='Archive uploader')
    parser.add_argument('--env', default='.env', help='Path to env file')
    parser.add_argument('--hash', action='store_true', help='Hash files for manifest')
    parser.add_argument('--manifest', default='exports/archive_manifest.json')
    parser.add_argument('--upload', action='store_true', help='Upload via S3-compatible endpoint')
    parser.add_argument('--prefix', default='archive/')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()

    load_dotenv(args.env, override=False)
    items = build_manifest(args.paths, hash_files=args.hash)
    out_path = write_manifest(items, args.manifest)
    print(f'manifest: {out_path} ({len(items)} files)')

    if not args.upload:
        return
    bucket = os.environ.get('CF_R2_BUCKET', '')
    endpoint = os.environ.get('CF_R2_ENDPOINT', '')
    access_key = os.environ.get('CF_R2_ACCESS_KEY_ID', '')
    secret_key = os.environ.get('CF_R2_SECRET_ACCESS_KEY', '')
    if not all([bucket, endpoint, access_key, secret_key]):
        raise SystemExit('missing R2 env vars for upload')
    res = upload_manifest_s3(
        items,
        bucket=bucket,
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        prefix=args.prefix,
    )
    print(json.dumps(res, indent=2))


if __name__ == '__main__':
    main()
