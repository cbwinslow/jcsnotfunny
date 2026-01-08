# SOPs (Standard Operating Procedures)

## Ingest (raw footage)

- Collect all camera files, audio tracks, and timecode logs
- Rename using format: `YYYYMMDD_episode_x_camera_A.ext` and place in `raw_videos/<episode>/`
- Generate proxy files for editing (ProRes/Cineform or h264 proxies)

## Rough Cut

- Create multicam sequence with labeled tracks
- Remove obvious dead air, long gaps, and redundant tangents

## Audio

- Normalize LUFS to -14 LUFS (podcast/streaming) for final render
- Clean noise, remove hums, use gating as needed

## Clip creation

- Create short clips 15–90s, captions burned or sidecar .srt/.vtt
- Export in 1080x1080 (IG), 1080x1350 (feed), and 1920x1080 (YT shorts)

## Deliverable naming

`<episode>-final.mp4`, `<episode>-audio.mp3`, `<episode>-clip-01.mp4`, `<episode>-transcript.vtt`

## Publishing

- Upload to YouTube and schedule the episode
- Publish show notes & transcript to website and post assets to socials
