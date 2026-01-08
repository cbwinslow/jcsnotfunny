# Repository Guidelines

## Project Structure & Module Organization
This repository stores Codex CLI runtime metadata rather than application code. Root-level configuration lives in `config.toml`, `config.json`, and `version.json`, which the CLI reads on startup. Session transcripts are grouped under `sessions/YYYY/MM/DD/*.jsonl`, while operational logs live in `log/codex-tui.log`. Treat `history.jsonl` and `internal_storage.json` as append-only archives; rotate them only after taking a backup.

## Build, Test, and Development Commands
There is no build pipeline; focus on validating configuration edits.
- `python -m json.tool config.json` validates JSON formatting.
- `python - <<'PY'` … `tomllib.loads(pathlib.Path("config.toml").read_text())` checks TOML with Python 3.11+.
- `codex --config config.toml` starts the CLI so you can confirm MCP reconnects and no new errors appear in `log/codex-tui.log`.

## Coding Style & Naming Conventions
Use two-space indentation in JSON and one setting per line in TOML files. Prefer lower_snake_case keys (for example, `sandbox_mode`, `approval_policy`) and single-quoted string literals in TOML. When documenting paths or commands, use absolute or repo-relative paths such as `sessions/2025/11/05/...` so others can copy them directly.

## Testing Guidelines
Rely on smoke tests: restart the CLI, trigger an MCP handshake, and inspect the tail of `log/codex-tui.log` for warnings. For larger edits, validate a representative session replay by copying a prior `.jsonl` entry into a new session file and confirming the tool rehydrates it.

## Commit & Pull Request Guidelines
Use Conventional Commit prefixes like `docs:`, `config:`, and `chore:`. Keep commits small and bundle related config edits with their validation notes. Pull requests should explain why the change is needed, reference related session dates when applicable, and include a short checklist of manual verifications (for example, "✅ CLI restart passes, ✅ model selection persists").

## Security & Configuration Tips
Never place API tokens directly in `auth.json`; use local secret stores and document placeholder keys instead. If you add new trusted project roots in `config.toml`, note whether they require heightened sandbox permissions and why. Before sharing logs, scrub user-identifying data from `sessions/**/*.jsonl` or provide redacted excerpts only.
