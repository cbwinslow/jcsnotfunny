# Knowledge Base — JCS Not Funny (Lightweight)

Purpose: concise, task-focused summaries and navigation for agents and developers. Use these docs as authoritative short-context for automation tasks, tests, and prompts.

How to use:
- Humans: read the short guides below for context and links to deeper docs.
- Agents/LLMs: prefer the short files for prompt context (< 500 words) and follow links to full docs as needed.

Contents:
- SHORTS_AUTOMATION.md — automation and pipeline summary for YouTube Shorts 🚀
- EDL_AUTOMATION.md — EDL selection rules and PoC details ✂️
- TRANSCRIPTION.md — transcribe & diarization summary, fixtures, and CI 📝
- MCP_SERVERS.md — MCP servers list, examples, and config notes 🤖
- AGENTS_TOOLS_INDEX.md — compact map of agents ↔ tools ↔ files 🔧
- knowledge_index.json — programmatic index for quick agent lookup (path/intent)

Notes & guidance
- Keep these files short and evergreen. For deep technical details, each page links to the canonical doc in `docs/` or relevant scripts/tests in the repo.
- When adding new automation, add a short summary to this KB and update `knowledge_index.json`.

---

If you want, I can also add a small script that loads `knowledge_index.json` and prints the most-relevant docs for a given keyword (useful for agents).
