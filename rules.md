# Master Rules Documentation

## Overview
This master document organizes all podcast production and social media management rules. Each section contains non-negotiable standards and absolutes for the podcast production system.

## Core Documentation Structure

### 🎯 Production Foundations
- **[Podcast Norms & Absolutes](./docs/rules/podcast-norms.md)** - Core principles, brand identity, and non-negotiable workflows
- **[Technical Standards](./docs/rules/technical-standards.md)** - Audio/video specifications, equipment requirements, and quality control

### 📱 Social Media Operations  
- **[Social Media Standards](./docs/rules/social-media-standards.md)** - Platform-specific rules, content strategy, and community management

### 🤖 Agent & Automation Rules
- **[Agent Guidelines](./agents.md)** - Agent configurations, capabilities, and workflow standards

## Quick Reference Absolutes

### Content Quality (NON-NEGOTIABLE)
✅ **Audio**: 48kHz/24-bit minimum, -16 LUFS target  
✅ **Video**: 4K premium, 1080p minimum, 60fps preferred  
✅ **Speaker Focus**: 95% AI accuracy on camera switching  
✅ **Content Authenticity**: Preserve conversation integrity  

### Workflow Requirements (MANDATORY)
✅ **Episode Length**: 60-120 min main, 15-30 min mini  
✅ **Sponsor Cap**: 10% maximum runtime, natural placement  
✅ **Simultaneous Release**: 30-minute window across platforms  
✅ **3-2-1 Backup**: 3 copies, 2 media types, 1 offsite  

### Social Media Standards (REQUIRED)
✅ **Posting Frequency**: 3-8 posts/day, minimum 3/week  
✅ **Response Times**: 2 hours mentions, 24 hours DMs  
✅ **Content Mix**: 40% episode promo, 30% engaging, 20% tour, 10% sponsor  
✅ **Engagement Standards**: Authentic, humorous, boundary-respecting  

### Performance Metrics (MINIMUMS)
✅ **Engagement Rate**: 3%+ across all platforms  
✅ **Completion Rate**: 70%+ for video content  
✅ **Sponsor ROI**: 3:1 minimum return on ad spend  
✅ **Follower Growth**: 5%+ monthly growth  

---

## Decision Matrix for Scenarios

### 🚨 Crisis Response
| Level | Response Time | Handler | Escalation |
|-------|---------------|----------|------------|
| 1 (Minor) | 4 hours | Social Media Manager | No |
| 2 (Moderate) | 2 hours | Senior Team | Yes |
| 3 (Major) | 1 hour | Executive Team | Yes |
| 4 (Critical) | Immediate | Legal/PR | Immediate |

### 📋 Content Approval Workflow
1. **Rough Cut** (48hrs) → 2. **Fine Cut** (48hrs) → 3. **Sponsor Review** (72hrs) → 4. **Final Sign-off** (12hrs)

### 🎬 Episode Production Pipeline
1. **Recording** → 2. **Backup** → 3. **Analysis** → 4. **Editing** → 5. **Review** → 6. **Distribution** → 7. **Promotion**

---

## Platform-Specific Quick Guides

### Twitter/X
- **Limits**: 280 chars (420 Premium)
- **Optimal**: 9-11 AM, 1-3 PM, 7-9 PM EST
- **Hashtags**: Max 3, mix trending + branded
- **Media**: 16:9 video, high-quality images

### Instagram  
- **Mix**: 60% Reels, 25% Posts, 15% Stories
- **Reels**: 15-60 seconds, trending audio
- **Hashtags**: 15-30, all categories
- **Stories**: 5-10 per day, 2-3 sessions

### TikTok
- **Length**: 15-60 seconds optimal
- **Content**: 40% clips, 30% trends, 20% behind scenes
- **Posting**: 7-9 PM EST peak
- **Audio**: Use trending sounds when appropriate

### YouTube
- **Titles**: Max 60 chars, include episode + guest
- **Descriptions**: 500+ chars, timestamps, links
- **Thumbnails**: 1280x720, high contrast
- **Upload**: Consistent day/time, schedule preferred

### LinkedIn
- **Frequency**: 3-5 posts/week, max 1/day
- **Tone**: Professional, industry insights
- **Articles**: 500-1000 words long-form
- **Hashtags**: 3-5 professional, industry-specific

---

## Brand Identity Non-Negotiables

### Visual Standards
- **Color Palette**: Consistent across all platforms
- **Logo Usage**: Approved variations only, clear space rules
- **Typography**: Brand fonts only, consistent hierarchy
- **Imagery Style**: Professional, authentic, on-brand

### Voice & Tone
- **Primary**: Authentic, conversational, curious
- **Secondary**: Slightly edgy but inclusive
- **Humor**: Witty, not offensive, self-aware
- **Authority**: Confident but humble, evidence-based

### Content Values
- **Truth-Seeking**: Facts over opinions, research-backed
- **Curiosity-Driven**: Ask questions, explore deeply
- **Entertainment**: Engaging, fun, memorable
- **Inclusivity**: Respectful, diverse perspectives welcome

---

## Technical Infrastructure Requirements

### Hardware Minimums
- **Cameras**: 4K, 60fps, professional lenses
- **Audio**: 48kHz/24-bit, XLR connections
- **Storage**: 50TB RAID, 3-2-1 backup strategy
- **Network**: Gigabit internet, backup connection

### Software Standards
- **Video**: Adobe Creative Cloud or equivalent
- **Audio**: Pro Tools or Logic Pro
- **Project**: Asana/Trello for management
- **Communication**: Slack internal, approved external platforms

### Security Requirements
- **Data Encryption**: AES-256 for sensitive data
- **Access Control**: Role-based with 2FA mandatory
- **Network**: Firewall, VPN, intrusion detection
- **Compliance**: GDPR, copyright, privacy laws

---

## Quality Assurance Checklist

### Pre-Release ✅
- Audio levels normalized to -16 LUFS
- Video exported in correct formats
- All metadata accurate and complete
- Subtitles/captions 99% accurate
- Brand elements properly placed

### Post-Release ✅
- Analytics tracking configured
- Social media posts scheduled
- Backup completed and verified
- Archive process documented
- Performance monitoring active

---

## Document Version Control

- **Last Updated**: 2025-01-07
- **Review Cycle**: Monthly or after major changes
- **Approval Required**: Executive team for major changes
- **Distribution**: All team members must acknowledge receipt

---

## Emergency Contact Protocol

### Production Issues
- **Audio/Video Engineer**: On-call 24/7
- **Social Media Manager**: 2-hour response SLA
- **Executive Producer**: 1-hour escalation path
- **Legal/PR**: Immediate for critical issues

### Technical Support
- **IT/Infrastructure**: 4-hour response SLA
- **Cloud Services**: 99.9% uptime guaranteed
- **Backup Systems**: Daily verification required
- **Recovery Testing**: Quarterly drills mandatory

---

## Test Coverage & Automation Requirements

### Testing Standards
✅ **New Features = New Tests**: Every new workflow, provider, or tool must ship with unit tests and workflow validation tests  
✅ **Failure-Mode Tests**: API errors, missing credentials, malformed metadata, scheduling drift covered  
✅ **Validation First**: Tests must cover created, scheduled, delivered, and verified states  
✅ **Regression Guardrails**: Bug fixes require regression tests  

### Documentation Standards
✅ **Docs Sync**: New workflows update relevant docs with usage examples  
✅ **Config Templates**: Update example files when providers/settings change  
✅ **Agent Updates**: New automation requires updated agent instructions  

### Quality Assurance
✅ **Test Naming**: Scoped and descriptive (e.g., `tests/test_social_workflows.py`)  
✅ **Coverage Maintenance**: New endpoints/fields expand test coverage  
✅ **Diagnostics**: Tests surface actionable errors with clear causes