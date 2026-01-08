# Issue: Implement X (Twitter) client module

**Description**
Implement `scripts/providers/x_client.py` with OAuth flow, posting, and error handling. Add unit tests and integration instructions.

**Checklist**

- [ ] Implement OAuth1 or OAuth2 user-posting flow
- [ ] Implement `post_text` with retry & backoff, error handling for 429/5xx
- [ ] Add unit tests (mocked HTTP) and an optional integration smoke test
- [ ] Add docs for required secrets and scopes in `docs/SOCIAL_AUTOMATION.md`

**Labels**: type/automation, priority/high
**Estimate**: 1–2 days
