import os
import pathlib
import subprocess


def test_checker_ignores_bare_token_links(tmp_path: pathlib.Path) -> None:
    # a bare token like 'parsed_args' should not fail the checker
    md = tmp_path / "t.md"
    md.write_text("[link](parsed_args)")

    res = subprocess.run(["python3", "scripts/doc_link_checker.py", "--root", str(tmp_path)], capture_output=True, text=True)
    assert res.returncode == 0, f"Checker failed on bare token: {res.stdout}\n{res.stderr}"
