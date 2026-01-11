# Copilot / Agents Instructions (project-specific)

This file gives concise, actionable guidance to Copilot-style AI agents and automation jobs that will modify or add code in this repository.

## Quick goals
- Automate ingest/transcription → generate short clips → publish to YouTube / website.
- Support autonomous GitHub issue processing via the production swarm.
- Keep code compatible with Python 3.13+, use `uv sync` for dev setup and `pytest` for tests.

## How to run locally (short)
- Install: `pip install uv` then `uv sync` to create the virtualenv and install deps.
- Activate: `source .venv/bin/activate`.
- Run tests: `pytest -q` (CI uses `Pytest: Run Tests` task and `.github/workflows/tests.yml`).
- Format & lint: run `isort`, `black .` and `flake8` (there is a VS Code task `Format & Lint`).
- Launch full autonomous workflow (requires GitHub env vars):
  ```bash
  export GITHUB_TOKEN=...
  export GITHUB_REPO_OWNER=cbwinslow
  export GITHUB_REPO_NAME=jcsnotfunny
  python launch_production_swarm.py
  ```

## Critical files & where to look (quick map)
- agents/ — actual agent implementations (extend `BaseAgent` from `agents/base_agent.py`).
- agents_config.json — authoritative agent configs, tool schemas, and environment placeholders.
- mcp-servers/ — MCP server implementations (automation server, supermemory, etc.).
- scripts/ & crews/ — ready-made pipelines and crew workflows (e.g. `scripts/youtube_shorts_pipeline.py`, `crews/youtube_shorts_crew.py`).
- docs/ — architecture, prompts, toolset design and SOPs (very useful for domain rules and examples).
- tests/ — unit and e2e tests: follow existing test structure and use fixtures in `tests/fixtures` for media.
- .github/workflows/ — CI and pipeline triggers (watchers, package_agents, content_pipeline, e2e-smoke etc.).
- configs/ — canonical config templates (`configs/agents/`, `configs/toolsets/`, `configs/rules/`, `configs/memories/`). Use `scripts/sync_agent_configs.py` to generate `agents_config.json` used at runtime.

## Environment & secrets (what to use, don’t hardcode)
- Commonly required env vars: `GITHUB_TOKEN`, `YOUTUBE_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `SUPERMEMORY_API_KEY`, `INSTAGRAM_ACCESS_TOKEN`, `TWITTER_BEARER_TOKEN`.
- CI uses GitHub Secrets; local dev should use `.env` or shell exports. **Never commit secrets to the repo.**

## Agent development pattern (do this)
1. Create `agents/<your_agent>.py` that subclasses `BaseAgent`.
2. Add your agent entry and `system_prompt`, `role`, `tools` to `agents_config.json`.
3. Implement tools with `RobustTool` wrappers where appropriate (see `agents/content_automation_agent.py`).
4. Add unit tests under `tests/test_<your_agent>.py` and use mocks/fixtures (see `agents/automation_testing_framework.py` for testing patterns).
5. Add package/packaging step if needed (GitHub workflow: `package_agents.yml`).

Example (minimal):
- In code: `class MyAgent(BaseAgent): ...`
- In agents_config.json: add `{"name":"MyAgent","role":"...","system_prompt":"...","tools": {}}`

## Pipeline & CI notes (what automation expects)
- Watchers & triggers: `watch-youtube-trigger-transcribe.yml` triggers transcription for new uploads.
- E2E smoke tests exist (`.github/workflows/e2e-smoke.yml`) — changes that alter pipelines must keep or update e2e smoke tests.
- Packaging agents uses `package_agents.yml` (push to `agents/**` triggers artifact creation).

## Tests & testing guidance (project-specific)
- Tests mock external APIs; prefer using existing fixture patterns in `tests/fixtures` and `agents/automation_testing_framework.py`.
- For integration tests that call YouTube/Cloudflare, add an opt-in dry-run mode or use recorded fixtures; CI runs specific integration workflows in GitHub Actions.
- Run an individual test: `pytest tests/test_youtube_shorts_pipeline_integration.py -q`.

## Helpful prompts & examples for agent actions
- "Ingest new footage from `raw_videos/2026-01-07_ep5`, generate proxies and add metadata JSON with timestamps and camera mappings."
- "Transcribe `raw_videos/ep5/audio_master.wav` to WebVTT and create time-coded highlights for top 10 keywords."
- "Create a new agent `MyAgent` that detects sponsor mentions: add `agents/my_agent.py`, register in `agents_config.json`, and add unit tests using the fixtures pattern."

## Project-specific conventions & gotchas
- Python 3.13 and async-first style; include type hints where applicable.
- Heavy-lifting I/O and network calls should be abstracted and testable (see `scripts/providers/*` and `mcp-servers/*`).
- Use platform-specific format helpers in `tools`/`toolsets` (YouTube formatting and sound loudness rules are encoded in docs under `docs/toolsets`).
- Do not bypass the `agents_config.json` for agent config - it's the single source of truth for agent roles, prompts, and credentials placeholders.

## MCP Servers (local & hosted)
- Local servers: `mcp-servers/automation-server`, `mcp-servers/social-media-manager`, `mcp-servers/media-processing-mcp`.
- Hosted memory MCP: `https://mcp.supermemory.ai/mcp`.
- Config location: `configs/mcp_servers.json` and workspace hints: `.vscode/settings.json`.
- Use `.vscode/tasks.json` entries to start servers locally for development or `docker compose up` for containers.

## Where to find prompt templates and examples
- `docs/prompts/` — enhanced prompts and templates for YouTube, social, and audio tasks.
- `.github/COPILOT_PROMPTS.md` — ready-to-use Copilot prompts for common actions.
- `docs/CONFIG_MANAGEMENT.md` — how config is centralized, synced, validated, and backed up (canonical configs live under `configs/`).

---
If anything above is unclear or missing, tell me which part you want expanded (running a specific workflow, writing tests, or adding a new agent) and I’ll refine the instructions. ✨
