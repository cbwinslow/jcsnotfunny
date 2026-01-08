---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Centralized Configuration Management'
labels: enhancement, type/automation, configuration
assignees: ''

---

This issue is for refining and activating centralized configuration management across the project.

**Description:**
Hardcoded values and inconsistent configuration approaches reduce flexibility and maintainability. This task focuses on leveraging existing `load_config` functions (`scripts/automation_runner.py` context) and establishing a robust, centralized system for all configuration parameters.

**Subtasks (from tasks.md):**
- Externalize all hardcoded configuration values (e.g., `PLATFORM_ENDPOINTS`, `PLATFORM_ENV_KEYS`, `POST_TEMPLATES`, thresholds) to central configuration files (`configs/*.json/yml`).
- Enhance `load_dotenv` (from `social_workflows`) or create a new utility to specifically check for and report on missing required environment variables for the platforms in use.
