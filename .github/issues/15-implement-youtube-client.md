# Issue: Implement YouTube client (uploads)

**Description**
Implement `scripts/providers/youtube_client.py` with OAuth2 refresh flow, resumable upload for long videos and Shorts, and tests.

**Checklist**

- [ ] Integrate `google-auth` credential refresh and `googleapiclient` uploads
- [ ] Implement `upload_short` and `upload_full` methods and return canonical URLs
- [ ] Add unit tests (mocking) and an optional integration test using a staging channel
- [ ] Document scopes and GitHub Secrets required

**Labels**: type/automation, priority/high
**Estimate**: 1–3 days
