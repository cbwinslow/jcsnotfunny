# Website & YouTube Integration

This doc explains the YouTube watcher and how to wire it to the `transcribe-integration.yml` workflow.

Overview

- `scripts/integrations/youtube_watcher.py` polls a channel for recent uploads and calls a callback for newly discovered videos.
- The watcher stores a small state file (`.youtube_watcher_state.json` by default) to avoid duplicate triggers.
- Use the OAuth helper (`scripts/integrations/get_youtube_token.py`) to obtain `YT_REFRESH_TOKEN` or set `YT_API_KEY` for lightweight access.

Polling vs Webhook

- Polling is simpler and works without additional hosting (our watcher supports it). Use polling for low-frequency checks (e.g., every 5–15 minutes).
- Webhooks (push notifications) require an HTTP endpoint and a more complex setup (recommended for production larger-scale deployments).

Triggering `transcribe-integration.yml`

- The watcher callback can call `gh workflow run transcribe-integration.yml -f video_id=<video_id>` once you have `gh` and appropriate tokens configured. Example message printed by the watcher includes instructions.
- Alternatively, call the GitHub REST API `POST /repos/:owner/:repo/actions/workflows/transcribe-integration.yml/dispatches` with a repo-scoped token.

Security & secrets

- Store `YT_API_KEY` or OAuth client secrets and refresh tokens in Bitwarden or GitHub Secrets (see `docs/SECRETS.md`).
- The watcher can be run locally by the owner, or deployed in a dev VM using Docker Compose (TODO: add compose service).

Next steps

- Add behavior to call `transcribe-integration.yml` automatically (requires decisions on token storage & minimal scopes).
- Add a worker service in `docker-compose.yml` and a `systemd` unit example for dev deployment (see tasks.md).
