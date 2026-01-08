# SOP - Live Production, OBS, and Multicast

## Purpose
Define the live production setup for recording and streaming with OBS and multicast targets.

## Tools
- OBS Studio for capture, scene switching, and local recording.
- Optional: Stream Deck or hotkeys for scene control.
- Multicast options: Restream, StreamYard, Castr, or OBS Multi-RTMP plugin.

## Inputs
- Run-of-show, final sponsor reads, stream keys, and platform titles/descriptions.

## Outputs
- Live stream on target platforms and a local recording for post-production.

## Checklist - Pre-Show Technical Check
- [ ] Power and UPS check for all critical devices.
- [ ] Mics connected and tested; no clipping or distortion.
- [ ] Input levels set (peaks around -6 dB, average -18 dB).
- [ ] Headphone monitoring active; no echo or latency.
- [ ] Camera framing and focus confirmed.
- [ ] Lighting check (key, fill, backlight).
- [ ] Internet check (upload speed, wired connection preferred).
- [ ] Local recording enabled and tested.
- [ ] Streaming destination test page opened.
- [ ] Backup recording path confirmed (local disk and/or SD card).
- [ ] Scene transitions verified.

## Checklist - OBS Setup
- [ ] Create scenes: Intro, Main, Guest, Screen Share, Break, Outro.
- [ ] Add audio sources: host mic, guest mic, system audio.
- [ ] Add video sources: cameras, capture cards, remote guest feed.
- [ ] Add overlays: lower thirds, sponsor banner, logos.
- [ ] Configure recording settings: 1080p, high bitrate, local file naming.
- [ ] Configure stream settings: RTMP endpoint(s), stream key(s).
- [ ] Save and export the OBS profile and scene collection.

## Checklist - Multicast Setup
- [ ] Create scheduled events for each platform.
- [ ] Collect RTMP URLs and stream keys.
- [ ] Use a multicast service or OBS Multi-RTMP plugin.
- [ ] Match titles/descriptions across platforms.
- [ ] Add thumbnails and tags where supported.

### Target Platforms (configure as available)
- YouTube Live
- Twitch
- X Live (Twitter Live / Periscope RTMP)
- Facebook Live
- Instagram Live (via approved Live Producer or third-party bridge)
- Kick
- TikTok Live
- LinkedIn Live

## Checklist - Go Live
- [ ] Start local recording first.
- [ ] Go live to multicast target.
- [ ] Confirm each platform shows live status.
- [ ] Monitor CPU/GPU and dropped frames in OBS.
- [ ] Assign chat moderation and cues.

## Checklist - Post-Live
- [ ] Stop stream, then stop local recording.
- [ ] Verify the local recording file exists and plays back.
- [ ] Save chat logs (if needed).
- [ ] Archive OBS scene collection changes.
- [ ] Log any issues in a post-mortem note.

## Placeholders
- [PLACEHOLDER: preferred multicast service]
- [PLACEHOLDER: standard OBS profile settings]
