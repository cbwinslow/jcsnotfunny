import json
import os
import pathlib
import subprocess


def test_doc_links_no_new_broken_links(tmp_path: pathlib.Path) -> None:
    # Run the doc link checker and capture output
    root = os.getcwd()
    res = subprocess.run(
        ["python3", "scripts/doc_link_checker.py", "--root", root, "--exclude", ".git,venv,.venv,node_modules,website/.next"],
        capture_output=True,
        text=True,
    )

    # The checker exits with non-zero when broken links are found. We allow existing broken links by
    # using a whitelist file that lists known broken links (one per line in the format:
    # path/to/file.md -> relative/path/to/target.md#anchor)
    whitelist_path = os.path.join(root, "docs", "doc_link_whitelist.txt")
    if os.path.exists(whitelist_path):
        with open(whitelist_path, "r") as f:
            whitelist = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    else:
        whitelist = []

    # If there are broken links, the script prints them. We'll assert that any printed broken link
    # appears in the whitelist so PRs don't introduce new failures.
    if res.returncode != 0:
        stdout = res.stdout + "\n" + res.stderr
        broken_lines = [ln.strip() for ln in stdout.splitlines() if "->" in ln]
        # Normalize whitespace and strip trailing diagnostic text (e.g., "(target not found: ...)")
        def normalize_broken(ln: str) -> str:
            ln = " ".join(ln.split())
            # remove leading '- ' if present
            if ln.startswith("- "):
                ln = ln[2:]
            # strip trailing parenthetical diagnostics
            if " (target not found:" in ln:
                ln = ln.split(" (target not found:", 1)[0]
            return ln

        broken_normalized = [normalize_broken(ln) for ln in broken_lines]

        unknown = [ln for ln in broken_normalized if ln not in whitelist]
        assert not unknown, f"Found new broken links not in whitelist:\n{json.dumps(unknown, indent=2)}"

    # If exit code is 0, nothing to assert
