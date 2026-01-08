---
name: Feature Request
about: Suggest an idea for this project
title: 'New Tool: Automated Broken Link Checker (link_checker.py)'
labels: new_feature, type/automation, area/seo, area/website, area/quality
assignees: ''

---

This issue is for implementing a new tool, `link_checker.py`, for automated broken link checking.

**Description:**
Broken links harm SEO, user experience, and overall site quality. This task involves creating a tool that automatically identifies and reports broken internal and external links on the website.

**Subtasks (from plan):**
- Implement a `link_checker.py` (new tool) to regularly crawl the site for broken internal and external links and report findings.

**Acceptance Criteria:**
- The `link_checker.py` script can crawl the entire website and identify broken links.
- A report of broken links is generated, including the URL of the broken link and the page it was found on.
- The script can be integrated into a CI/CD pipeline or run on a schedule.
- Findings are integrated with the `notification-and-reporting` job for alerts.
