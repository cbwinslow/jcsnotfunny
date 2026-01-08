# SOP - Editing and Post-Production

## Purpose
Define editing steps for episodes, including audio mix, captions, and exports.

## Tools
- Capture: OBS Studio (recording and scene switching).
- Editing: [PLACEHOLDER: primary NLE, e.g., DaVinci Resolve or Premiere].
- Audio cleanup: [PLACEHOLDER: plugin suite or DAW].
  - Presets: `configs/audio_presets.yml` and `docs/SOPS_AUDIO_MIXING.md`.

## Inputs
- Local recording files (video and audio), sponsor read notes, run-of-show.

## Outputs
- Final episode video and audio masters, captions, and metadata.

## Checklist - Ingest and Organization
- [ ] Copy all files to `raw_videos/<episode>/`.
- [ ] Verify file integrity and check durations.
- [ ] Rename assets using `YYYY-MM-DD_episode_<number>_<source>.ext`.
- [ ] Generate proxies if needed for editing performance.
- [ ] Create project folder structure (video, audio, graphics, exports).

## Checklist - Edit Passes
- [ ] Assemble rough cut (remove dead air and tangents).
- [ ] Sync external audio and align waveforms.
- [ ] Insert sponsor reads at agreed timestamps.
- [ ] Add titles, lower thirds, and overlays.
- [ ] Create final color pass and LUT application.

## Checklist - Audio Mix
- [ ] Noise reduction and de-essing as needed.
- [ ] Normalize to target loudness (see `docs/DELIVERABLES.md`).
- [ ] Check true peaks and avoid clipping.
- [ ] Listen to full episode for pops and dropouts.

## Checklist - Captions and Transcript
- [ ] Generate initial transcript (automated).
- [ ] Review and correct names and technical terms.
- [ ] Export captions in VTT/SRT.
- [ ] Store transcript file in the episode folder.

## Checklist - Exports
- [ ] Export full episode master (H.264, 1080p).
- [ ] Export audio-only version (MP3/WAV).
- [ ] Export thumbnails and stills if needed.
- [ ] Verify playback on a separate device.

## Placeholders
- [PLACEHOLDER: export presets and bitrate targets]
- [PLACEHOLDER: audio processing chain]
