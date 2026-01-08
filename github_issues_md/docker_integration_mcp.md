---
name: Feature Request
about: Suggest an idea for this project
title: 'Setup: Docker Integration for MCP Servers using docker-compose'
labels: setup, type/automation, mcp, docker
assignees: ''

---

This issue is for setting up Docker integration for all MCP servers using `docker-compose.yml`.

**Description:**
To ensure efficient and consistent deployment and management of the MCP servers, especially in development and CI/CD environments, they will be containerized and orchestrated using Docker Compose.

**Subtasks (from plan):**
- Create a `Dockerfile` for `mcp-servers/social-media-manager/`.
- Create a `Dockerfile` for `mcp-servers/media-processing-mcp/`.
- Create a `docker-compose.yml` file in the project root to orchestrate the deployment of `social-media-mcp`, `media-processing-mcp`, and `supabase-mcp`.
- Ensure appropriate port mappings and environment variable pass-through are configured in `docker-compose.yml`.
- Add `Dockerfile` for `mcp-servers/social-media-manager`.
- Add `Dockerfile` for `mcp-servers/media-processing-mcp`.

**Acceptance Criteria:**
- All MCP servers can be successfully started and managed using `docker-compose up`.
- Environment variables are correctly passed to the Docker containers.
- MCP servers within containers are accessible and their tools can be invoked by the Gemini CLI.
