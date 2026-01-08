---
name: Feature Request
about: Suggest an idea for this project
title: 'New Tool: Automated Podcast RSS Feed Generation (scripts/rss_generator.py)'
labels: new_feature, type/automation, area/website
assignees: ''

---

This issue is for implementing a new tool, `scripts/rss_generator.py`, to automatically generate and update the podcast's RSS feed.

**Description:**
A crucial component for podcast distribution is a dynamically updated RSS feed. This task involves creating a script that automatically generates and updates the RSS feed whenever a new episode is published, ensuring listeners always have access to the latest content.

**Subtasks (from tasks.md):**
- Implement `scripts/rss_generator.py` (new tool) to automatically generate and update the podcast's RSS feed upon new episode distribution.

**Acceptance Criteria:**
- The script should parse episode metadata and generate a valid RSS XML feed.
- The RSS feed should be updated automatically after `scripts/publish.py` successfully pushes a new episode to the website.
- The generated RSS feed should include all necessary elements for podcast directories (e.g., iTunes, Spotify).
- Unit tests should verify the correctness of the generated XML structure.
