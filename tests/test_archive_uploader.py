from scripts.archive_uploader import build_manifest


def test_build_manifest(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("data")
    items = build_manifest([str(file_path)], hash_files=False)
    assert len(items) == 1
    assert items[0].path.endswith("sample.txt")
    assert items[0].size_bytes == 4
