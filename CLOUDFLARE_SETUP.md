# Cloudflare & CDN Setup

Recommend Cloudflare Pages (static site) + Cloudflare CDN for assets.

Steps:

1. Create Cloudflare account and add domain (e.g., jaredsnotfunny.com)
2. Configure Pages project connecting to GitHub repo
3. Add DNS records and enable proxying where needed
4. Configure caching rules for `assets/` and video proxies
5. Add a Cloudflare Worker or signed URL approach if you need restricted access for some assets
6. Optimize media assets for Cloudflare CDN

Secrets:

- `CF_PAGES_API_TOKEN` — store in GitHub Secrets
- `CF_ACCOUNT_ID` — store in GitHub Secrets

Cache Rules:

- Cache static assets for 1 year: `assets/*`
- Cache HTML for 1 day: `*.html`
- Bypass cache for dynamic content: `api/*`

Security Headers:

- Content-Security-Policy: `default-src 'self'`
- Strict-Transport-Security: `max-age=63072000; includeSubDomains; preload`
- X-Content-Type-Options: `nosniff`
- X-Frame-Options: `DENY`
