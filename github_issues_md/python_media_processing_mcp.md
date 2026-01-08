---
name: Feature Request
about: Suggest an idea for this project
title: 'Implement: Python-based Media Processing MCP Server (transcription & video analysis)'
labels: new_feature, type/automation, area/editing, mcp
assignees: ''

---

This issue is for implementing a new Python-based Media Processing MCP Server to expose transcription and video analysis tools.

**Description:**
This new MCP server will wrap existing Python scripts (`scripts/transcribe.py` and `scripts/video_analyzer.py`) to provide AI agents with capabilities for transcribing media and analyzing video content.

**Subtasks (from plan):**
- Create a new directory: `mcp-servers/media-processing-mcp/`.
- Inside, create `server.py` using a Python MCP framework (e.g., `FastMCP`).
- Implement the `transcribe_media` tool, wrapping `scripts/transcribe.py` functionality.
- Implement the `analyze_video_content` tool, wrapping `scripts/video_analyzer.py` functionality.
- Add a `Dockerfile` for containerization.

**Tools Proposed:**
*   `transcribe_media`: Wraps `scripts/transcribe.py` to generate VTT/JSON transcripts.
    *   **Input Schema:** `audio_path: string`, `output_dir: string`, `backend: 'whisper' | 'api'`, `model: string?`
    *   **Output Schema:** `vtt_path: string`, `json_path: string`
*   `analyze_video_content`: Wraps `scripts/video_analyzer.py` to perform speaker detection, engagement scoring, and other video analysis.
    *   **Input Schema:** `video_path: string`, `output_path: string`, `speaker_detection: boolean`, `engagement_scoring: boolean`
    *   **Output Schema:** `analysis_json_path: string`

**Prerequisites:**
*   Python (>=3.11) installed.
*   Dependencies: `FastMCP`, `whisper`, `requests`, `opencv-python`, `moviepy`, `pydub`, `librosa`, `numpy`, `scipy`.
*   `ffmpeg` installed and available on PATH.

**Required Environment Variables:**
*   `TRANSCRIBE_BACKEND`, `TRANSCRIBE_API_URL`, `TRANSCRIBE_API_KEY` (if using API backend for transcription)

**Acceptance Criteria:**
- The Python Media Processing MCP server runs successfully in a Docker container.
- The `transcribe_media` tool successfully transcribes media and produces VTT/JSON output when invoked via MCP.
- The `analyze_video_content` tool successfully analyzes video and produces analysis JSON when invoked via MCP.
- Appropriate error handling is implemented for both tools.
- Unit tests cover the tool definitions and script integrations.
