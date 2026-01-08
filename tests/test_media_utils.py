from utils.media_utils import checksum
import tempfile


def test_checksum(tmp_path):
    p = tmp_path / 'foo.txt'
    p.write_bytes(b'hello world')
    h = checksum(str(p))
    assert len(h) == 64
