---
name: Feature Request
about: Suggest an idea for this project
title: 'Enhance: Automated Live Stream Pre-Check (scripts/diagnostics.py)'
labels: enhancement, type/automation, area/ops
assignees: ''

---

This issue is for implementing automated pre-checks for live streams using `scripts/diagnostics.py`.

**Description:**
To ensure a smooth live streaming experience, it's crucial to verify the health of all streaming infrastructure components before going live. This task involves automating these checks.

**Subtasks (from tasks.md):**
- Create a GitHub Actions workflow to run `scripts/diagnostics.py --live` before live streams to ensure infrastructure health.
- Integrate warnings/failures with the `notification-and-reporting` job.

**Additional Automation Opportunities (from previous analysis):**
- **Continuous Monitoring & Alerting:** Run `diagnostics.run_snapshot` on a recurring schedule and integrate any `warn` or `failed` statuses with the `notification-and-reporting` job for alerts.
- **Automated Troubleshooting Integration:** Integrate `diagnostics.run_snapshot` into error handling or post-failure analysis steps of streaming/recording workflows.
- **Dynamic Thresholds/Baselines:** Externalize `min_free_gb` and `min_growth_kb` to a configuration file.
- **Expand Network Interface Checks:** Enhance `check_network_interfaces` to check latency to external services or bandwidth.
