---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Social Media Publishing & Workflows Integration and Expansion'
labels: enhancement, type/automation, area/social_media
assignees: ''

---

This issue covers the integration and expansion of various social media publishing and workflow scripts.

**Description:**
The project has robust `scripts/social_media_apis.py` for API interaction, but these need to be integrated into `scripts/social_publish.py` and orchestrated by `scripts/social_workflows.py` to activate live publishing, expand scheduling, and enhance analytics. Redundant clients should be consolidated.

**Subtasks (from tasks.md):**
- **Activate Live Publishing:** Integrate `SocialMediaManager` (from `scripts/social_media_apis.py`) into `scripts/social_publish.py`'s `schedule_post` function to handle actual posting/scheduling.
- **Expand Scheduling:** Extend `SocialMediaManager.schedule_cross_post` to include LinkedIn and TikTok scheduling (if API supports).
- **Expand Analytics:** Complete `SocialMediaManager.get_analytics_summary` to include X, TikTok, and LinkedIn analytics.
- **Content Validation:** Add pre-posting content validation (e.g., character limits, media requirements) to `social_publish.py`.
- **Externalize Templates:** Move `POST_TEMPLATES` from `social_publish.py` to an external configuration file for dynamic loading.
- **Consolidate Clients:** Deprecate `scripts/providers/x_client.py` and `scripts/providers/youtube_client.py` where redundant, refactoring their uses to the more comprehensive `SocialMediaManager`.
- **Third-Party Scheduler (Optional):** Implement `scripts/providers/scheduler_client.py` if a unified third-party scheduling service is desired.

**Additional Automation Opportunities (from previous analysis):**
- **Robust Error Handling (within `SocialMediaManager`):** Implement comprehensive error handling, logging, and retry mechanisms for cross-platform operations.
- **Content Moderation/Validation:** Integrate checks for objectionable content, brand safety, and platform guidelines before publishing.
- **Dynamic Scheduling:** Implement more sophisticated scheduling logic (e.g., optimizing post times based on audience activity).
- **Automated API Key Rotation:** For enhanced security, explore automated rotation of API keys/tokens.
