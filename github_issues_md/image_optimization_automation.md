---
name: Feature Request
about: Suggest an idea for this project
title: 'New Tool: Image Optimization Automation (image_optimizer.py)'
labels: new_feature, type/automation, area/seo, area/website, area/assets
assignees: ''

---

This issue is for implementing a new tool, `image_optimizer.py`, for automated image optimization.

**Description:**
Large or unoptimized images can significantly slow down website loading times, negatively impacting user experience and SEO. This task involves automating the optimization of images used across the project.

**Subtasks (from plan):**
- Implement `image_optimizer.py` (new tool) to process images (thumbnails, social graphics) for web delivery (compression, lazy loading, responsive images, WebP format) within the asset pipeline.

**Acceptance Criteria:**
- The `image_optimizer.py` script can automatically process images from specified directories.
- Images are compressed without significant loss of quality.
- Images are converted to modern formats (e.g., WebP) where appropriate.
- Responsive image variants are generated (if applicable).
- The asset pipeline integrates image optimization (e.g., after `thumbnail_agent.py` generates images).
