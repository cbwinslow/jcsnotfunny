# Copilot / Agent Prompts (examples)

Use these prompts with Copilot-style agents or automated runners. Keep them focused and include expected outputs and file paths.

- Ingest agent

  - "Ingest `raw_videos/ep05/` — verify checksums, generate low-res proxies at `working_projects/ep05/proxies/`, and write `ingest_meta.json` including camera map and timecode."

- Transcribe agent

  - "Transcribe `working_projects/ep05/audio_master.wav` to `edited/ep05/transcript.vtt` and `edited/ep05/transcript.json`. Use Whisper small model if available."

- Clip generator

  - "Generate 6 short clips from `working_projects/ep05/ep05.mp4` using `edited/ep05/transcript.vtt` and output to `edited/ep05/clips/` as `clip-001.mp4`... Include captions sidecar `clip-001.vtt`."

- Social publish
  - "Render social posts for platforms X, Instagram, and YouTube Short for episode `ep05` using metadata in `website/content/episodes/ep05.json`, schedule them 1 hour after the episode publish time. Provide the rendered text for each platform in a JSON file."

Be explicit with expected outputs and file names to make the prompts deterministic and testable.
