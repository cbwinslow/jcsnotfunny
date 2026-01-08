# SOP - Backups, Archives, and Storage Strategy

## Purpose
Define how raw footage, masters, and social assets are backed up and archived.

## Inputs
- Raw footage, project files, exports, captions, and metadata.

## Outputs
- Redundant backups and an organized archive structure.

## Checklist - Local Storage and Archival
- [ ] Store raw footage under `raw_videos/<episode>/`.
- [ ] Store project files under `projects/<episode>/`.
- [ ] Store masters and exports under `exports/<episode>/`.
- [ ] Store social media exports under `exports/<episode>/social/`.
- [ ] Use consistent naming conventions from `docs/SOPS_POST_PRODUCTION.md`.
- [ ] Compress long-term archives to save space.

## Checklist - Backup Process
- [ ] Keep at least two local copies (primary + backup drive).
- [ ] Maintain one off-site or cloud copy.
- [ ] Verify backup integrity monthly (spot-check playback).
- [ ] Log backup dates and storage locations.

## Storage Options (Discussion)
### Option A - Local Server with Redundant Drives
- Buy a small server or NAS and install multiple HDDs (8-20 TB each).
- Use RAID (RAID5/RAID6 or RAIDZ) for drive redundancy.
- Store compressed archives and social media exports.
- Pros: Lower long-term cost, fast local access.
- Cons: Upfront hardware cost, requires maintenance and monitoring.

### Option B - Cloud Object Storage
- Providers: Backblaze B2, AWS S3 + Glacier, Wasabi, Google Cloud Storage.
- Pros: Off-site redundancy, scalable, no hardware maintenance.
- Cons: Monthly cost and egress fees for large restores.
  - Note: Cloudflare R2 is recommended for predictable egress and CDN proximity.

### Option C - Hybrid (Recommended)
- Local server or NAS for primary storage + cloud for off-site redundancy.
- Keep social media archives in the cloud for quick sharing.
- Automate nightly syncs and weekly integrity checks.

## Recommendation (Draft)
- Purchase a dedicated server or NAS with multiple HDDs.
- Use compressed archives for older episodes.
- Add a cloud backup target for redundancy and disaster recovery.

## Placeholders
- [PLACEHOLDER: storage vendor selection]
- [PLACEHOLDER: target capacity and budget]
- [PLACEHOLDER: backup schedule and tool choice]
