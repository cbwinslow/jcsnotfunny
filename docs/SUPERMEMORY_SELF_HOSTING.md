# Supermemory Self-Hosting (Enterprise)

This repository can integrate with a self-hosted Supermemory API. The official self-hosting flow is Cloudflare Workers-based and requires an enterprise deployment package from Supermemory.

> Source: https://supermemory.ai/docs/deployment/self-hosting#self-hosting

## Scope and prerequisites

- Enterprise-only: request the deployment package from Supermemory.
- The package includes your `NEXT_PUBLIC_HOST_ID`, compiled bundle, and `deploy.ts`.
- Cloudflare account with Workers enabled.
- PostgreSQL with pgvector, SSL, and connectivity from Cloudflare Workers.
- LLM provider keys (OpenAI required).
- Resend API key if using email notifications.

## Recommended local layout

Keep the deployment package outside version control.

```bash
deployments/
  supermemory/   # unpack the enterprise zip here (gitignored)
```

## Cloudflare prerequisites

Create a Cloudflare API token with:

- Account:AI Gateway:Edit
- Account:Hyperdrive:Edit
- Account:Workers KV Storage:Edit
- Account:Workers R2 Storage:Edit

Enable Workers in your Cloudflare dashboard and choose a workers.dev subdomain.

## Database prerequisites

Provide a PostgreSQL connection string in `DATABASE_URL`:

```
postgresql://username:password@hostname:port/database
```

The database must support pgvector and allow connections from Cloudflare.

## Environment variables

Copy the package template and fill required values:

```bash
cd deployments/supermemory
cp packages/alchemy/env.example .env
$EDITOR .env
```

Required keys (per Supermemory docs):

- `NODE_ENV`
- `NEXT_PUBLIC_HOST_ID`
- `BETTER_AUTH_SECRET`
- `BETTER_AUTH_URL`
- `DATABASE_URL`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
- `OPENAI_API_KEY`
- `RESEND_API_KEY`

Generate `BETTER_AUTH_SECRET` with:

```bash
openssl rand -base64 32
```

Optional keys include `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`,
OAuth provider keys, and connector credentials (Google Drive, OneDrive, Notion).

## Deploy

Run the deployment script from the package directory:

```bash
cd deployments/supermemory
bun ./deploy.ts
```

## Notes for MCP

If you want MCP memory tools to target your self-hosted API, use the Supermemory
client setup instructions from `https://app.supermemory.ai` and apply your
self-hosted API base URL in their installer/config where supported.

## MCP client install (hosted)

For hosted MCP (not self-hosted), install the Supermemory MCP server per client:

```bash
npx -y install-mcp@latest https://mcp.supermemory.ai/mcp --client claude --oauth yes --yes
```

Swap `--client` for other agents (e.g., `codex`, `cursor`, `cline`, `windsurf`).
