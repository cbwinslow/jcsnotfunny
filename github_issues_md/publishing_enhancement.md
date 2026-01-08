---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Implement full YouTube upload and website deployment in Publishing (scripts/publish.py)'
labels: enhancement, type/automation, area/website
assignees: ''

---

This issue is for fully implementing YouTube video uploads and automated website deployment triggers within the `scripts/publish.py` script.

**Description:**
The `scripts/publish.py` currently contains placeholder functions for YouTube upload and website updates. This task involves replacing these placeholders with functional integrations.

**Subtasks (from tasks.md):**
- Fully implement `upload_to_youtube` leveraging `scripts/social_media_apis.py`'s `YouTubeAPI`.
- Implement automated website deployment triggers (e.g., GitHub API to trigger `deploy_site.yml` or Cloudflare Pages API).

**Additional Automation Opportunities (from previous analysis):**
- **YouTube Metadata Generation:** Ensure `metadata_generator.py` produces all necessary metadata (title, description, tags, privacy status) for YouTube uploads and scheduling.
- **Website Content Generation:** Expand `push_episode_to_website` to generate full episode pages (e.g., Markdown or HTML) directly consumable by the website static site generator.
- **Error Handling:** Robust error handling for YouTube API failures, network issues, and website deployment failures.
- **Status Reporting:** Report the success or failure of YouTube uploads and website deployments back to the main workflow.
