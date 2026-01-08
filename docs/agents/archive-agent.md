# Archive Agent

## Overview
Creates archive manifests and uploads files to S3-compatible storage (R2/B2).

## Inputs
- Files or directories to archive
- Storage credentials (via `.env`)

## Outputs
- `exports/archive_manifest.json`
- Uploaded objects in the archive bucket

## Usage
```bash
python scripts/archive_uploader.py --hash --manifest exports/archive_manifest.json raw_videos/ep01 exports/ep01
```

## Notes
- Install `boto3` to enable uploads.
- Use the manifest to verify integrity during restores.
