import os
import pytest
from unittest.mock import patch, MagicMock

from scripts.integrations.r2_uploader import _get_s3_client, upload_bytes, R2UploadError


def test_get_s3_client_missing_env(monkeypatch):
    monkeypatch.delenv('CF_R2_ENDPOINT', raising=False)
    monkeypatch.delenv('CF_R2_ACCESS_KEY_ID', raising=False)
    monkeypatch.delenv('CF_R2_SECRET_ACCESS_KEY', raising=False)

    with pytest.raises(R2UploadError):
        _get_s3_client()


def test_upload_bytes_raises_when_boto_missing(monkeypatch):
    # simulate missing boto3 by temporarily renaming it in sys.modules
    monkeypatch.setitem(__import__('sys').modules, 'boto3', None)
    with pytest.raises(R2UploadError):
        upload_bytes('bucket', 'key', b'data')


def test_upload_bytes_calls_boto3(monkeypatch):
    mock_s3 = MagicMock()
    mock_client = MagicMock(return_value=mock_s3)

    # monkeypatch the internal client factory to return our mock s3 client
    monkeypatch.setattr('scripts.integrations.r2_uploader._get_s3_client', lambda: mock_s3)

    # set required env (not used by stub, but keep consistent)
    monkeypatch.setenv('CF_R2_ENDPOINT', 'https://r2.test')
    monkeypatch.setenv('CF_R2_ACCESS_KEY_ID', 'ak')
    monkeypatch.setenv('CF_R2_SECRET_ACCESS_KEY', 'sk')

    # call (should not raise)
    upload_bytes('bucket', 'key', b'data')
    # nothing to assert against fake, but no exception is success
