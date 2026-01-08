# Live Director Agent

## Overview
The Live Director Agent monitors audio levels and switches camera scenes in OBS to focus on the active speaker.

## Approach
1. Capture audio meter levels for each speaker input.
2. Detect the loudest active speaker above a threshold.
3. Switch OBS scenes using OBS WebSocket.
4. Apply a cooldown to prevent rapid switching.

## Required Tools
- OBS Studio with obs-websocket enabled.
- Optional: Advanced Scene Switcher plugin for fallback.
- A stable per-speaker audio input (separate tracks recommended).
  - Optional: an audio meter source or OBS WebSocket audio-level API.

## Operating Notes
- Do not switch on every syllable; use a cooldown (3-8 seconds).
- Use a noise gate to reduce false triggers.
- Maintain a manual override scene for the host.

## Next Steps
- Implement a real OBS WebSocket client.
- Add optional face detection to override audio-only switching.
