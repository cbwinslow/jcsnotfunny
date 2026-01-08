# Assets Inventory — Jared's Not Funny Podcast

This document tracks existing public assets and missing assets to collect for the website and branding.

## Known Accounts (Need Verification/Connection)

| Platform  | Account Name       | Status      | Notes                               |
| --------- | ------------------ | ----------- | ----------------------------------- |
| YouTube   | @JaredsNotFunny    | **MISSING** | Need channel ID and API credentials |
| Facebook  | @JaredsNotFunny    | **MISSING** | Need page ID and access token       |
| Instagram | @jaredsnotfunny    | **MISSING** | Need business account ID            |
| Twitter/X | @JaredsNotFunny    | **MISSING** | Need API credentials                |
| TikTok    | @jaredsnotfunny    | **MISSING** | Need API credentials                |
| LinkedIn  | Jared Christianson | **MISSING** | Need API credentials                |

### Environment Variables Required

```bash
# YouTube API
YT_API_KEY=
YT_CLIENT_ID=
YT_CLIENT_SECRET=
YT_REFRESH_TOKEN=
YT_CHANNEL_ID=

# Facebook Pages API
FACEBOOK_PAGE_ID=
FACEBOOK_PAGE_ACCESS_TOKEN=

# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ID=

# Twitter / X API
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_SECRET=
X_BEARER_TOKEN=

# TikTok API
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
```

---

## Website Assets

### Current Website Structure

- **Project**: `website/` (Next.js)
- **Pages**: `/`, `/tour`, `/gallery`, `/contact`
- **Components**: Layout, Header, Footer, Hero, TourDates, Gallery, Contact

### Existing Website Components

| Component | Path                              | Status | Notes                                 |
| --------- | --------------------------------- | ------ | ------------------------------------- |
| Layout    | `website/components/Layout.js`    | ✓      | Basic layout wrapper                  |
| Header    | `website/components/Header.js`    | ✓      | Navigation links                      |
| Footer    | `website/components/Footer.js`    | ✓      | Copyright footer                      |
| Hero      | `website/components/Hero.js`      | ✓      | Welcome section - needs real content  |
| TourDates | `website/components/TourDates.js` | ✓      | Hardcoded placeholder dates           |
| Gallery   | `website/components/Gallery.js`   | ✓      | References `/images/image1.jpg`, etc. |
| Contact   | `website/components/Contact.js`   | ✓      | Contact form - non-functional         |

### Tour Dates (Placeholder Data)

```json
[
  { "date": "2026-02-15", "location": "New York, NY", "venue": "Madison Square Garden" },
  { "date": "2026-02-20", "location": "Los Angeles, CA", "venue": "Staples Center" },
  { "date": "2026-02-25", "location": "Chicago, IL", "venue": "United Center" }
]
```

**Note**: These are placeholder dates. Real tour dates need to be gathered.

---

## Visual Assets Needed

| Asset                         | Status      | Priority | Notes                             |
| ----------------------------- | ----------- | -------- | --------------------------------- |
| Logo (SVG/PNG)                | **MISSING** | HIGH     | Primary brand logo                |
| Host Headshots                | **MISSING** | HIGH     | Jared Christianson photos         |
| Show Banner                   | **MISSING** | MEDIUM   | Website hero banner               |
| Episode Thumbnails            | **MISSING** | MEDIUM   | Template for episodes             |
| Gallery Images                | **MISSING** | HIGH     | `website/public/images/` is empty |
| Social Media Profile Pictures | **MISSING** | HIGH     | Consistent across platforms       |
| Social Media Cover Images     | **MISSING** | MEDIUM   | Platform-specific banners         |

### Image Locations

- Website images: `website/public/images/`
- Currently missing: `image1.jpg`, `image2.jpg`, `image3.jpg`

---

## Show/Episode Information

| Field            | Status      | Notes                                 |
| ---------------- | ----------- | ------------------------------------- |
| Show Name        | ✓           | "Jared's Not Funny" / "JCS Not Funny" |
| Host Name        | ✓           | Jared Christianson                    |
| Location         | ✓           | Roanoke, VA                           |
| Episode Archive  | **MISSING** | Need to gather episode links          |
| YouTube Playlist | **MISSING** | Need channel URL                      |
| Podcast RSS Feed | **MISSING** | Apple Podcasts, Spotify, etc.         |

---

## Known URLs (to Verify)

| URL        | Status                                       | Notes                  |
| ---------- | -------------------------------------------- | ---------------------- |
| Website    | `https://jareds-not-funny.pages.dev/`        | Cloudflare Pages       |
| Repository | `https://github.com/cbwinslow/jcsnotfunny`   | This repo              |
| YouTube    | `https://youtube.com/channel/{{CHANNEL_ID}}` | Need actual channel ID |
| Facebook   | `https://facebook.com/{{PAGE_ID}}`           | Need actual page ID    |

---

## API/Integration Configuration Files

| File                           | Purpose                       |
| ------------------------------ | ----------------------------- |
| `.env.example`                 | Environment variable template |
| `configs/social_providers.yml` | Social media publish settings |
| `configs/master_settings.json` | Project configuration         |
| `agents_config.json`           | Agent tool configurations     |

---

## Content Templates

| Template      | Location                             | Notes                   |
| ------------- | ------------------------------------ | ----------------------- |
| Social Posts  | `templates/social_post_templates.md` | YouTube, Twitter, etc.  |
| Guest Profile | `docs/templates/guest_profile.md`    | Guest information       |
| Sponsor Read  | `docs/templates/sponsor_read.md`     | Sponsor script template |
| Run of Show   | `docs/templates/run_of_show.md`      | Show rundown template   |

---

## Missing Assets Checklist

### High Priority

- [ ] Host headshot (professional photo of Jared Christianson)
- [ ] Podcast logo (vector format preferred)
- [ ] Gallery images (3-5 photos for website)
- [ ] Verified YouTube channel URL
- [ ] Verified Facebook page URL

### Medium Priority

- [ ] Social media profile pictures (consistent branding)
- [ ] Episode thumbnail template
- [ ] Tour dates (actual upcoming shows)
- [ ] Podcast platform links (Apple Podcasts, Spotify, etc.)

### Low Priority

- [ ] Show banner/hero image
- [ ] Behind-the-scenes photos
- [ ] Guest photos archive
- [ ] Merchandise images

---

## Legal/IP

| Item                  | Status      | Notes                           |
| --------------------- | ----------- | ------------------------------- |
| Trademark (Show Name) | **UNKNOWN** | Check USPTO if needed           |
| Trademark (Logo)      | **UNKNOWN** | Check USPTO if needed           |
| Photo Usage Rights    | **UNKNOWN** | Confirm licenses for all images |
| Music/Sound Effects   | **UNKNOWN** | Identify royalty-free sources   |

---

## Next Steps

1. **Gather visual assets from host**: Request headshots, logo files, gallery photos
2. **Verify social accounts**: Search for existing accounts using podcast name
3. **Set up API credentials**: Complete `.env` file with real credentials
4. **Update website content**: Replace placeholder data with real tour dates, links, etc.
5. **Create image assets**: Design/produce missing visual assets
