# Social Automation — MCP vs Direct API

This document describes the architecture and decision matrix for social publish automation.

## Two supported patterns

1. MCP Agent Server (Managed)
   - A single, trusted agent endpoint receives a publish request and handles provider-specific logic.
   - Pros: Centralized logic, easier to rotate credentials, offload rate-limits and retries.
   - Cons: Requires running/maintaining a server; additional security considerations.

2. Direct API clients (Local)
   - The runner (CI/agent) uses provider SDKs (Twitter/X, Facebook/IG, YouTube) to publish content.
   - Pros: Simpler to reason about for small scale, fewer moving parts.
   - Cons: Token management across jobs and runners; provider quotas.

## Recommended approach
- Start with direct API mode for quick wins (X/Twitter + YouTube short) using the `scripts/mcp_publish.py --mode api` path.
- If usage grows, add an MCP agent server and switch mode to `mcp` in `configs/social_providers.yml`.

## Security & credentials
- Store all API secrets in repository Secrets (for GH Actions) and in a `.env` for local development (see `.env.example`)
- Prefer short-lived tokens and refresh flows (YouTube OAuth refresh tokens, Twitter OAuth2 flows)
- Limit scope of tokens to necessary actions (publish, not full admin)

## Error handling & retries
- MCP server should implement exponential backoff and idempotency keys for publish requests
- When using local API mode, scripts must check provider HTTP responses and retry transient failures (429, 5xx)

## Testability
- Unit tests (rendering, template validation) should run locally without credentials
- Integration smoke tests should be run in a staging project with test credentials and scheduled in CI

## Example prompts for Copilot/Agents
- "Render social posts for episode `ep05` and schedule to `x,instagram` using metadata in `website/content/ep05.json`"
- "Publish clips to YouTube Shorts and schedule text posts via Buffer using the short URLs returned from YouTube"

## Next steps
- Create provider-specific modules (X client, IG client, YouTube client) with common interface.
- Add GH Action to run `scripts/mcp_publish.py` in `mode=api` for manual dispatch or as part of the episode publish job.
