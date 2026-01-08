# Jared's Not Funny — Production Repository

This repo contains production workflows, SOPs, scripts, and website scaffolding to support Jared Christianson's podcast and related content creation. Built with Python 3.13+ and managed using uv for modern, fast package management.

## Quick Start

1. **Install uv**: `pip install uv` (or follow [uv installation guide](https://github.com/astral-sh/uv))
2. **Clone and setup**: `uv sync` to install dependencies
3. **Activate environment**: `source .venv/bin/activate`

## Project Structure

- `agents/` — AI agent implementations and configurations
- `docs/` — SOPs, agent documentation, and checklists
- `scripts/` — automation scripts (ingest, transcode, clip generation, social media)
- `website/` — Next.js static site for episodes, tour dates, SEO
- `tests/` — comprehensive test suite
- `mcp-servers/` — Model Context Protocol server implementations
- `configs/` — configuration files and templates
- `utils/` — shared utilities and helpers
- `validators/` — data validation and quality assurance
- `.github/` — issue templates, labels, and GitHub Actions

## Key Documentation

- **[Rules](./rules.md)** — Production standards and non-negotiable workflows
- **[Agents](./agents.md)** — AI agent configurations and capabilities
- **[ROADMAP](./ROADMAP.md)** — Development milestones and deliverables
- **[AGENTS](./AGENTS.md)** — Legacy agent documentation (being migrated)

## Development

This project uses:

- **Python 3.13+** with type hints and modern async patterns
- **uv** for lightning-fast package management and virtual environments
- **pytest** for comprehensive testing (95%+ coverage target)
- **Black + Ruff** for code formatting and linting

Read `ROADMAP.md` for milestones and deliverables.
