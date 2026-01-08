# SOP - Remote Editing and File Bridge

## Purpose
Enable post-production when the editor does not have local access to the recording machine.

## Inputs
- Raw recordings, proxy files, project files, and metadata.

## Outputs
- Accessible proxies for editing and a reliable path to full-resolution media.

## Recommended Flow
1. Record on-site and save masters to local storage.
2. Generate proxy files (lower bitrate) and upload to shared storage.
3. Edit using proxies, then relink to full-res for final export.
4. Upload final masters back to shared storage.

## File Bridge Options
### Option A - Cloudflare R2 + Proxies (Recommended)
- Upload proxies to R2 for fast remote access.
- Keep full-res masters on the on-site server/NAS.
- Use a simple manifest file to map proxy names to masters.

### Option B - Sync Tool (Syncthing/Resilio/Nextcloud)
- Continuous sync between on-site server and editor workstation.
- Best for teams that need live access to the entire project.

### Option C - Shipping Drives
- Use encrypted drives for large batch transfers.
- Keep checksums for integrity validation.

## Checklist - Proxy Workflow
- [ ] Create proxies in 720p or 1080p with matching timecode.
- [ ] Upload proxies to R2 or shared storage.
- [ ] Generate a manifest file (JSON or CSV).
- [ ] Confirm editor can download and open the project.
- [ ] After edits, relink to full-res for final export.

## Placeholders
- [PLACEHOLDER: proxy bitrate and codec]
- [PLACEHOLDER: shared storage URL or sync tool]
