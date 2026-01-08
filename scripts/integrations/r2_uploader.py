"""Simple uploader to Cloudflare R2 (S3-compatible) with boto3 fallback.

Environment variables used:
- CF_R2_ACCESS_KEY_ID
- CF_R2_SECRET_ACCESS_KEY
- CF_R2_ENDPOINT
- CF_R2_BUCKET

If boto3 is not available the uploader raises an informative error.
"""
from __future__ import annotations

import io
import logging
import os
from typing import Optional

logger = logging.getLogger("r2_uploader")
logging.basicConfig(level=logging.INFO)


class R2UploadError(RuntimeError):
    pass


def _get_s3_client():
    try:
        import boto3
        try:
            from botocore.client import Config
        except Exception:
            # Provide a minimal Config fallback for test environments where botocore stub may not provide Config
            class Config:
                def __init__(self, **kwargs):
                    pass
    except Exception as e:  # pragma: no cover - external dependency
        raise R2UploadError("boto3 is required for R2 uploads: pip install boto3") from e

    endpoint = os.environ.get("CF_R2_ENDPOINT")
    access_key = os.environ.get("CF_R2_ACCESS_KEY_ID")
    secret = os.environ.get("CF_R2_SECRET_ACCESS_KEY")

    if not endpoint or not access_key or not secret:
        raise R2UploadError("CF_R2_ENDPOINT, CF_R2_ACCESS_KEY_ID and CF_R2_SECRET_ACCESS_KEY must be set")

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        config=Config(signature_version="s3v4"),
    )
    return s3


def upload_bytes(bucket: str, key: str, data: bytes, content_type: Optional[str] = None) -> None:
    """Upload bytes to R2 bucket under `key`."""
    s3 = _get_s3_client()
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=data, **extra)
        logger.info("Uploaded %s to %s/%s", len(data), bucket, key)
    except Exception as e:
        logger.exception("Failed to upload to R2: %s", e)
        raise R2UploadError("Failed to upload to R2") from e


def upload_text(bucket: str, key: str, text: str, content_type: Optional[str] = "text/csv") -> None:
    upload_bytes(bucket, key, text.encode("utf-8"), content_type=content_type)
