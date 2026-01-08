---
name: Feature Request
about: Suggest an idea for this project
title: 'New Tool: Automated Sitemap Generation & Submission (sitemap_generator.py)'
labels: new_feature, type/automation, area/seo, area/website
assignees: ''

---

This issue is for implementing a new tool, `sitemap_generator.py`, to automate the generation and submission of the website's sitemap.

**Description:**
An up-to-date sitemap (`sitemap.xml`) is crucial for search engines to discover and index all relevant content on the website. This task involves automating its creation and ensuring it is submitted to search engines.

**Subtasks (from plan):**
- Implement `sitemap_generator.py` (new tool) to automatically generate and keep `sitemap.xml` up-to-date with all content (especially new episode pages).
- Integrate with Google Search Console API for automated submission or ensure `robots.txt` is updated.

**Acceptance Criteria:**
- The `sitemap_generator.py` script successfully generates a valid `sitemap.xml` file reflecting all website content.
- The sitemap is automatically updated when new content (e.g., episodes) is added.
- The sitemap is discoverable by search engines (e.g., linked in `robots.txt`).
- Optional: Automated submission to Google Search Console is implemented.
