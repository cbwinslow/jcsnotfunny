# SOP - Secrets and Configuration Management

## Purpose
Define how credentials are stored and loaded for streaming and social automation.

## Inputs
- Platform credentials, API tokens, RTMP stream keys.

## Outputs
- A secure local `.env` and a validated `configs/master_settings.yml`.

## Storage Policy
- Store credentials in Bitwarden (preferred) or Cloudflare Secrets for Workers.
- Never commit secrets to git. Use `.env.example` as the template.
- Use `configs/master_settings.yml` to define which env keys are required.
  - Optional: use Bitwarden CLI to export a `.env` on trusted machines.
  - Optional: use Cloudflare `wrangler secret put` for Worker secrets.

## Checklist - Local Setup
- [ ] Copy `.env.example` to `.env`.
- [ ] Pull values from Bitwarden into `.env`.
- [ ] Confirm `configs/master_settings.yml` points to the correct env keys.
- [ ] Verify OBS and RTMP targets load with the expected profile.
- [ ] Run `python -m scripts.cli credentials --mode offline` to confirm env coverage.
- [ ] Add automation provider tokens (thumbnail/SEO) if used.
- [ ] Confirm `configs/automation_tools.yml` reflects the chosen providers.

## Checklist - CI or Automation
- [ ] Store API tokens in GitHub Actions secrets (if used).
- [ ] Use Cloudflare Secrets for Worker and R2 credentials.
- [ ] Confirm no secrets appear in logs or crash dumps.

## Placeholders
- [PLACEHOLDER: Bitwarden vault collection name]
- [PLACEHOLDER: authorized maintainers]
