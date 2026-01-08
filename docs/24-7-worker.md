# 24/7 Worker Runbook & Quick Start

This document explains how to run the worker locally, deploy on a VM with Docker Compose, and the expected behavior.

## Quick start (local, dev)

1. Create a `.env` with minimal variables:
   - `GITHUB_FETCHER_FALLBACK=./dev/tasks.json` (sample task list)
   - `GITHUB_REPO_OWNER=cbwinslow`
   - `GITHUB_REPO=jcsnotfunny`
   - `GITHUB_TOKEN=<token>` (optional for propose-only comments)

2. Build and run locally:
   - docker compose -f agents/docker-compose.yml build
   - docker compose -f agents/docker-compose.yml up

3. Or run directly for development:
   - python -m agents.worker --run-once

## Health & metrics

- Health endpoint: `http://<host>:<port>/health` (worker prints port on startup); returns JSON with `status` and `uptime_seconds`.

- Prometheus metrics: default port `8001` exported by `prometheus_client` (`jcs_worker_uptime_seconds` gauge).

## Systemd VM deployment (example)

- Copy `agents/deploy/jcs-agent.service` to `/etc/systemd/system/jcs-agent.service` and edit paths as necessary.

- Enable and start: `systemctl enable --now jcs-agent`

## Safety & operation

- Default mode is `--propose-only`: the agent will post comments or create draft PRs rather than auto-claim or close issues.

- To enable full automation later, set `propose_only` to false and ensure the `GITHUB_TOKEN` has the correct scopes.

## Troubleshooting

- Check container logs: `docker compose -f agents/docker-compose.yml logs -f`.

- Health endpoint and Prometheus metrics help identify liveness and uptime issues.
