# Website snapshot: Jared's Not Funny (https://www.jaredsnotfunny.com/)

Fetched: 2026-01-08 UTC

Summary of fetched content

- Site: Google Sites hosted (site contains "Page updatedGoogle Sites").
- Primary links discovered:
  - Linktree: [linktr.ee/jaredsnotfunny](https://linktr.ee/jaredsnotfunny) (upcoming shows)
  - YouTube channel: [youtube.com/@JaredsNotFunny](https://www.youtube.com/@JaredsNotFunny) (podcast episodes)
  - TikTok: [tiktok.com/@jaredsnotphunny](https://www.tiktok.com/@jaredsnotphunny) (stand-up)
  - Other social links embedded in header/footer and link lists.
- Robots.txt: found and contains content-signal headers. Key lines:

```
# BEGIN Cloudflare Managed content
User-Agent: *
Content-signal: search=yes,ai-train=no
Allow: /
...
User-agent: GPTBot
Disallow: /
# END Cloudflare Managed Content
```

Notes:

- Robots file explicitly sets `ai-train=no` and disallows GPTBot and several other crawlers; it allows `search=yes` and `Allow: /` for general crawlers.
- No `sitemap.xml` was found at `/sitemap.xml` (HTTP 404).

Recommendation: store this snapshot in the repo for traceability and obey content-signal rules when building search/AI features.
