# Supermemory MCP Server

This MCP server provides persistent memory via Supermemory.

## Local run (npx)

```bash
npx @iflow-mcp/supermemoryai_supermemory-mcp@latest
```

## Docker Compose

Use the `supermemory-mcp` service in `docker-compose.yml`.

## Environment variables

- `SUPERMEMORY_API_KEY` (required for self-hosting)
- `SUPERMEMORY_PROJECT` (optional project scope)

## Notes

The `@iflow-mcp/supermemoryai_supermemory-mcp` package is MCP v1; prefer the latest setup instructions from `https://app.supermemory.ai`.
For enterprise self-hosting on Cloudflare Workers, follow `docs/SUPERMEMORY_SELF_HOSTING.md`.
