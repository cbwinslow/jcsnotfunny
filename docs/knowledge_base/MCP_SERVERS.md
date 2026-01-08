# MCP Servers — Quick Reference

Purpose: concise reference of MCP servers and configuration used by the project.

Known servers
- `mcp-servers/social-media-manager` (node stdio) — handles social posting tools
- `mcp-servers/media-processing-mcp` (python stdio) — transcribe / analyze tool wrappers
- `mcp-servers/supermemory-ai` (npx remote or hosted HTTP) — persistent memory
- `supabase` MCP (npx) — optional DB-backed MCP

Configs & files
- Repository config: `configs/master_settings.json` — contains `mcpServers` section (hosted URL for Supermemory)
- VSCode user config for MCP: `~/.config/Code/User/mcp.json` — add servers and default server
- Docker compose: `docker-compose.yml` includes MCP services for local testing
- Deployment: `.github/workflows/mcp-deployment.yml` builds and deploys MCP images

Usage tips
- For agents to use hosted Supermemory, set `mcpServers.supermemory.url` in `configs/master_settings.json` or prefer the `mcp-supermemory-http` server in user mcp.json
- When adding an MCP server, update `docs/knowledge_base/knowledge_index.json` to include the server and its intended usage


Related docs: `mcp-servers/supermemory-ai/README.md`, `AGENTS.md`, `.github/workflows/mcp-deployment.yml`
