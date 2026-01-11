# Doc Link Checker

This repository includes tooling to prevent new broken internal Markdown links from being introduced.

How it works:

- Run: `python3 scripts/doc_link_checker.py --root .` (use `--exclude` to skip folders like `.git`, `node_modules`, or `website/.next`).
- Known broken links are recorded in `docs/doc_link_whitelist.txt` to allow incremental cleanup — CI fails on *new* broken links only.

Permanent rules the checker follows (to avoid noisy failures):

- `file:line` references are accepted if the referenced file exists (the checker checks the file portion before `:`).
- Non-file schemes (e.g. `mdc:/`, `url:`) and bare tokens (e.g. `error`, `parsed_args`) are treated as non-file references and do not fail the check.
- Use `scripts/normalize_file_line_links.py` to rewrite `file:line` links in Markdown to canonical `file` links (this helps keep docs stable over time).

How to add exceptions:

- If you find a legitimate broken link that must remain for historical reasons, add a line to `docs/doc_link_whitelist.txt` of the form `path/to/file.md -> relative/path/to/target.md#anchor`.

CI:

- A GitHub Actions workflow (`.github/workflows/link-check.yml`) runs the checker on PRs and will block if new broken links are detected.

If you need help triaging the whitelist, open a small PR that fixes or documents the change you want and update the whitelist accordingly.
