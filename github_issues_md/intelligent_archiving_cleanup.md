---
name: Feature Request
about: Suggest an idea for this project
title: 'New Tool: Intelligent Archiving & Cleanup (scripts/archive_manager.py)'
labels: new_feature, type/automation, area/ops
assignees: ''

---

This issue is for implementing a new tool, `scripts/archive_manager.py`, for intelligent archiving and cleanup of project assets.

**Description:**
As the project generates numerous assets (raw footage, intermediate files, final outputs), an automated system for intelligent archiving and cleanup is essential to manage storage costs and maintain an organized workspace.

**Subtasks (from tasks.md):**
- Implement `scripts/archive_manager.py` (new tool) for intelligent archiving of assets (e.g., deleting intermediate files, moving to cheaper storage).

**Additional Automation Opportunities (from previous analysis):**
- Delete intermediate artifacts after a certain period to save storage.
- Move older raw footage to long-term, cheaper storage.
- Cleanup temporary files.
