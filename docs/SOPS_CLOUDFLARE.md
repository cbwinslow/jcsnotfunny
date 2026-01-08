# SOP - Cloudflare Platform Usage

## Purpose
Standardize how we use Cloudflare services for storage, streaming, and automation.

## Services and Use Cases
### R2 (Buckets)
- Store raw footage archives, masters, and social exports.
- Use lifecycle rules to move older files to low-cost storage.
- Keep one bucket for production, one for archives.
  - Use R2 for proxy sharing in the remote editing workflow.

### Stream (Video)
- Host clips and full episodes for embeds and internal review.
- Use signed URLs for private or pre-release assets.
- Generate thumbnails and previews for quick review.
  - Note: Stream is best for VOD; live streams still use platform RTMP.

### Images
- Store thumbnails and social images with auto-resize.
- Use variant URLs for platform-specific sizes.

### Workers
- Build lightweight APIs for scheduling, validation hooks, and asset indexing.
- Create a webhook relay for social publish results.

### AI
- Auto-generate clip titles, summaries, and tags.
- Create moderation summaries from chat logs or comments.

## Checklist - Setup
- [ ] Confirm Cloudflare account and project ownership.
- [ ] Create R2 buckets for `production` and `archive`.
- [ ] Enable Cloudflare Stream and Images.
- [ ] Create API tokens with least-privilege scopes.
- [ ] Store tokens in Bitwarden and/or Cloudflare Secrets.
- [ ] Configure keys in `.env` and `configs/master_settings.yml`.

## Checklist - Operations
- [ ] Upload masters to R2 after final export.
- [ ] Mirror critical assets to R2 and local storage.
- [ ] Use Stream for clip review and internal approvals.
- [ ] Use Images for thumbnails and site assets.

## Placeholders
- [PLACEHOLDER: R2 bucket naming conventions]
- [PLACEHOLDER: stream retention policy]
- [PLACEHOLDER: Worker endpoints and routing]
