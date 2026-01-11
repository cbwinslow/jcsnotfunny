import os
import pathlib
import subprocess


def test_checker_accepts_file_line_links(tmp_path: pathlib.Path) -> None:
    # create a dummy target file
    target = tmp_path / "subdir" / "file.js"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("console.log('ok')")

    # create a markdown file that links to file.js:123
    md = tmp_path / "test.md"
    md.write_text("[link](subdir/file.js:123)")

    res = subprocess.run(["python3", "scripts/doc_link_checker.py", "--root", str(tmp_path)], capture_output=True, text=True)
    # should exit 0 because file.js exists and file:line should be accepted
    assert res.returncode == 0, f"Checker failed on file:line link: {res.stdout}\n{res.stderr}"


def test_checker_ignores_non_file_schemes(tmp_path: pathlib.Path) -> None:
    md = tmp_path / "test2.md"
    md.write_text("[link](mdc:/rules/01.md)")

    res = subprocess.run(["python3", "scripts/doc_link_checker.py", "--root", str(tmp_path)], capture_output=True, text=True)
    # mdc: scheme is ignored and should not cause a failure
    assert res.returncode == 0, f"Checker failed on mdc: scheme: {res.stdout}\n{res.stderr}"
