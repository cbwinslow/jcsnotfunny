---
name: Feature Request
about: Suggest an idea for this project
title: 'Implement: Full YouTube Upload & Search in Node.js Social Media Manager MCP'
labels: enhancement, type/automation, area/social_media, mcp
assignees: ''

---

This issue is for fully implementing YouTube video upload and search functionality within the Node.js `social-media-manager` MCP server.

**Description:**
The `upload_to_youtube` tool in `mcp-servers/social-media-manager/server.js` is currently a placeholder, and `search_youtube_videos` has been added as a placeholder. This task involves replacing these placeholders with actual YouTube Data API v3 integration.

**Subtasks (from plan):**
- Replace the placeholder logic for `upload_to_youtube` with actual YouTube Data API v3 resumable upload functionality (Node.js client library like `googleapis` recommended).
- Replace the placeholder logic for `search_youtube_videos` with actual YouTube Data API v3 search functionality, allowing agents to search for videos by query, max results, order, and published date.

**Required Environment Variables:**
- `YOUTUBE_API_KEY`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

**Acceptance Criteria:**
- The `upload_to_youtube` tool successfully uploads a video to YouTube when invoked via MCP.
- The `search_youtube_videos` tool returns relevant search results from YouTube when invoked via MCP.
- Error handling for API calls is robust.
- Unit tests are implemented for both functionalities.
