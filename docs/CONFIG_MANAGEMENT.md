# Configuration Management & Governance

This document describes where to store and maintain the authoritative configuration for agents, tools, rules, and memories and how to guarantee they are used, referenced, validated, and backed up.

Core principles
- Canonical configuration lives under `configs/` (e.g. `configs/agents/`, `configs/toolsets/`, `configs/rules/`, `configs/memories/`). These files are the single source of truth.
- `agents_config.json` in repository root is generated from `configs/agents/*.json` via `scripts/sync_agent_configs.py` and consumed by agents at runtime.
- Agents should check environment variable `AGENTS_CONFIG_PATH` first and fall back to `configs/agents/agents_config.json` or `agents_config.json` (see `agents/base_agent.py` behavior).
- A validation step (`scripts/validate_configs.py`) verifies references between agents, tools, and rules and runs in CI on PRs and daily.
- Nightly backups of configs are produced and stored as build artifacts (`build/config-backups.tar.gz`) by the `validate_and_backup` workflow.

How to add or change configs
1. Add or update `configs/agents/<agent>.json` or relevant `configs/toolsets/<toolset>.json`.
2. Run `python scripts/sync_agent_configs.py` locally to generate `agents_config.json`.
3. Add or update tests under `tests/test_agent_configs.py` if you change schemas or references.
4. Open a PR; CI will validate and create an artifact backup automatically.

Making agents aware and consistent
- Agents should always read from `AGENTS_CONFIG_PATH` env var or `configs/agents/agents_config.json`. Base Agent supports this by default.
- Use the `scripts/validate_configs.py` to detect missing tool references early.
- Add unit tests that simulate the agent loading step to ensure your agent can find its tools and env vars.

Backup & Restore
- Backups are created nightly by CI and available under the build artifacts (see workflow `validate_and_backup.yml`).
- To restore, extract the relevant files from `build/config-backups.tar.gz` and open a PR with changes.

Governance checklist (PRs touching configs)
- [ ] Did you add or update `configs/` instead of directly editing `agents_config.json`?
- [ ] Did `scripts/sync_agent_configs.py` produce the expected `agents_config.json`?
- [ ] Did `scripts/validate_configs.py` pass with no warnings? (CI is configured to fail on validation warnings; ensure the validator returns exit code 0)
- [ ] Did you add/update unit tests for schema or reference changes?

Policy & Branch Protection
- Ensure the repository's branch protection rules require the `Validate & Backup` and `Integration Matrix` workflows to pass before merging to `main`.

