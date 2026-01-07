# Issue: Social Automation — MCP & API Providers

**Description**
Implement a robust social publish toolset that supports both MCP agent servers and direct provider APIs. Include provider modules, credential docs, retries, and a GH Action to dispatch posts.

**Checklist**
- [ ] Create `scripts/mcp_publish.py` (done)
- [ ] Add provider-specific modules (X, Instagram, YouTube) and interfaces
- [ ] Add `configs/social_providers.yml.example` (done)
- [ ] Add GH Action to dispatch social posts (`.github/workflows/social_publish.yml`) and make it configurable for `mode=mcp|api`
- [ ] Add tests and integration smoke test (done)
- [ ] Document flow in `docs/SOCIAL_AUTOMATION.md` (done)

**Labels**: type/automation, area/website, priority/high
**Estimate**: 2-4 days
