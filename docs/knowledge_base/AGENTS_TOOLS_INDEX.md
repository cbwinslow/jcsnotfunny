# Agents & Tools Index (compact)

Purpose: quick mapping of agent names → primary tools → main files to help agents and devs navigate.

- transcription_agent
  - tools: transcribe_audio, generate_captions
  - files: `scripts/transcribe.py`, `scripts/transcribe_agent/agent.py`
- funny_moment_agent
  - tools: analyze_transcript, identify_funny_clips
  - files: `agents/funny_moment_agent.py`, `scripts/auto_edit/edl_generator.py`
- video_editing_agent
  - tools: download_video, extract_audio, trim_video
  - files: `agents/video_editing_agent.py`, `scripts/clip_generator.py`
- social_media_manager
  - tools: post_to_twitter, post_to_instagram, upload_to_youtube
  - files: `mcp-servers/social-media-manager/server.js`, `scripts/mcp_publish.py`

Note: For each agent, use the `agents/` folder and `scripts/` helper scripts as authoritative sources.
