# Assistant Orchestrator

## Overview
The Assistant Orchestrator is a local digital assistant that summarizes current production status and routes tasks to available tools. It is designed to be extended with MCP or LLM integrations later.

## Core Capabilities
- Generate a status snapshot (configs, SOPs, open tasks).
- Summarize credential health (offline checks, optional live checks).
- Act as a central entry point for CLI and automation commands.

## CLI Usage
```bash
python -m scripts.cli assistant --format json
python -m scripts.cli assistant --include-credentials --format text
```

## Data Sources
- `configs/master_settings.json` or `configs/master_settings.yml`
- `configs/host_profiles.yml`
- `configs/audio_presets.yml`
- `docs/SOPS.md`
- `tasks.md`

## Extension Points
- Add MCP tools for scheduling, social publishing, and validation.
- Integrate voice input or chat UI on top of the status report.
- Add health checks for storage and streaming endpoints.
