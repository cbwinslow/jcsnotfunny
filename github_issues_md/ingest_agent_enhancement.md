---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Implement robust ingest logic for Ingest Agent (scripts/ingest.py)'
labels: enhancement, type/automation, area/editing
assignees: ''

---

This issue is for implementing robust ingest logic for the `scripts/ingest.py` script, which is part of the Ingest Agent.

**Description:**
The `scripts/ingest.py` currently serves as a placeholder. This task involves replacing the stub with a comprehensive ingest process that correctly handles raw media files, ensuring data integrity and proper metadata handling.

**Subtasks (from tasks.md):**
- Implement robust ingest logic including checksums, proxy generation, and comprehensive metadata extraction following `session_config.yml` schema.

**Acceptance Criteria (from tasks.md for Media Ingest & Metadata):**
- Ingest normalization unit tests pass and return canonical metadata for all supported inputs.
- All generated artifacts (EDL, transcripts, renders) include a `metadata.json` that references original checksums.

**Additional Automation Opportunities (from previous analysis):**
- **Automated Trigger for Episode Production:** Link the completion of a robust ingest process to automatically trigger the `episode-production.yml` workflow.
- **Input Validation:** Ensure that incoming raw media files meet expected formats and quality standards.
- **Error Handling & Reporting:** Implement robust error handling for corrupted files, incomplete transfers, or issues during proxy generation, and integrate with the `notification-and-reporting` job for alerts.
