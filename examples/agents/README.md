# Agents / Automation Examples

This folder contains example agent scripts and usage notes.

Agents included (stubs):

- `scripts/transcribe.py` — produce WebVTT and JSON transcript files
- `scripts/clip_generator.py` — generate clips from a source video and VTT
- `scripts/publish.py` — helper to push episode metadata to website and simulate YouTube upload
- `scripts/social_publish.py` — render social posts and schedule them (stub)

How to run locally (example):

1. Transcribe an audio file:
   ```bash
   python scripts/transcribe.py --input raw_videos/ep01/audio_master.wav --output edited/ep01/transcript.vtt
   ```
2. Generate clips:
   ```bash
   python scripts/clip_generator.py --input raw_videos/ep01/ep01.mp4 --transcript edited/ep01/transcript.vtt --outdir edited/ep01/clips
   ```
3. Prepare publish metadata and push to site:
   ```bash
   python scripts/publish.py  # ❤️ this is a stub; fill in your deploy steps
   ```
4. Schedule social posts:
   ```bash
   python scripts/social_publish.py  # renders and prints posts; integrate with API provider
   ```

Notes

- These are intentionally minimal to act as example POCs. Add API keys in environment variables and extend them to your infrastructure.
- Add tests and CI steps for each agent as you harden them.
