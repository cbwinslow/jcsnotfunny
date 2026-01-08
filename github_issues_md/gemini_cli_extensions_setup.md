---
name: Feature Request
about: Suggest an idea for this project
title: 'Setup: Gemini CLI Extensions for Cloudflare, PostgreSQL, and Supabase MCP'
labels: setup, type/automation, mcp
assignees: ''

---

This issue is for setting up and configuring the Gemini CLI extensions for Cloudflare, PostgreSQL, and Supabase MCP servers.

**Description:**
These extensions provide AI agents with direct access to Cloudflare services (R2, Workers, DNS), PostgreSQL databases, and Supabase projects through the Gemini CLI. This will streamline infrastructure interaction and data management.

**Subtasks (from plan):**
*   **Cloudflare MCP Extension:**
    *   Find the actual GitHub URL for the Cloudflare MCP Extension.
    *   Install the extension using `gemini extensions install <Actual_GitHub_URL_for_Cloudflare_MCP_Extension>`.
    *   Ensure `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set.
*   **PostgreSQL MCP Extension:**
    *   Install the extension using `gemini extensions install https://github.com/gemini-cli-extensions/postgres`.
    *   Ensure PostgreSQL connection environment variables (`PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`) are set.
    *   Set up Application Default Credentials (ADC).
*   **Supabase MCP Server (Node.js version):**
    *   Install and run the Supabase MCP server using `npx -y @supabase/mcp-server-supabase@latest`.
    *   Ensure `SUPABASE_ACCESS_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` are set.
    *   **(Security Note):** Remember this is recommended for development purposes only.

**Acceptance Criteria:**
- All specified Gemini CLI extensions are successfully installed and recognized by the Gemini CLI.
- AI agents can successfully invoke tools provided by these extensions (e.g., interact with Cloudflare R2, query PostgreSQL, manage Supabase data).
- All required environment variables are securely configured.
