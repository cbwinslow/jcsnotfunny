# Podcast Production Agents Configuration

## Overview
This document defines the specialized agents and their configurations for managing podcast production, social media, and content distribution operations.

## Core Agent Types

### 1. Video Production Agent
**Name**: `video_editor`  
**Model**: `gpt-4o-vision-preview`  
**Role**: Intelligent video editing and content optimization

**Capabilities**:
- Multi-angle camera switching using AI speaker detection
- Automatic focus tracking on active speakers
- Short-form content creation (60-120 seconds)
- Color grading and visual enhancement
- Dynamic overlays and branding
- Platform-specific optimization

**Tools**:
```json
{
  "video_analysis": {
    "description": "Analyze footage for optimal cutting points",
    "parameters": {
      "video_path": "string",
      "analysis_type": ["speaker_detection", "engagement_scoring", "optimal_cut_points"],
      "focus_threshold": "number"
    }
  },
  "smart_cut": {
    "description": "AI-powered camera angle switching",
    "parameters": {
      "input_video": "string", 
      "output_video": "string",
      "cutting_style": ["dynamic", "conservative", "aggressive"],
      "focus_speakers": "array"
    }
  },
  "create_short": {
    "description": "Generate platform-specific short content",
    "parameters": {
      "source_video": "string",
      "duration": "number",
      "focus_topic": "string",
      "platform": ["tiktok", "instagram", "youtube_shorts"],
      "captions": "boolean"
    }
  },
  "brand_overlay": {
    "description": "Add consistent branding elements",
    "parameters": {
      "video_path": "string",
      "brand_config": "object",
      "position": ["top_left", "bottom_right", "center"],
      "opacity": "number"
    }
  }
}
```

**Workflow**: `episode_edit` → `short_creation` → `optimization`

---

### 2. Audio Engineering Agent
**Name**: `audio_engineer`  
**Model**: `gpt-4o`  
**Role**: Professional audio production and enhancement

**Capabilities**:
- Noise reduction and audio cleanup
- Voice enhancement and equalization
- Sponsor read integration
- Multi-source audio balancing
- Platform-specific mastering

**Tools**:
```json
{
  "audio_cleanup": {
    "description": "Remove background noise and artifacts",
    "parameters": {
      "audio_file": "string",
      "noise_reduction_level": ["light", "medium", "aggressive"],
      "deessing": "boolean",
      "normalization": "boolean"
    }
  },
  "voice_enhancement": {
    "description": "Enhance vocal clarity and presence",
    "parameters": {
      "audio_file": "string",
      "preset": ["podcast", "interview", "narration"],
      "eq_settings": "object",
      "compression_ratio": "number"
    }
  },
  "sponsor_integration": {
    "description": "Seamlessly integrate sponsor content",
    "parameters": {
      "main_audio": "string",
      "sponsor_content": "object",
      "insertion_points": "array",
      "transition_style": ["hard_cut", "fade", "crossfade"],
      "volume_matching": "boolean"
    }
  },
  "master_output": {
    "description": "Finalize audio for distribution",
    "parameters": {
      "audio_file": "string",
      "target_lufs": "number",
      "platforms": ["spotify", "apple_podcasts", "youtube"],
      "metadata": "object"
    }
  }
}
```

**Workflow**: `cleanup` → `enhancement` → `sponsor_integration` → `mastering`

---

### 3. Social Media Management Agent
**Name**: `social_media_manager`  
**Model**: `gpt-4o`  
**Role**: Multi-platform content management and audience engagement

**Capabilities**:
- Cross-platform content scheduling
- Audience engagement and community management
- Performance analytics and optimization
- Content calendar management
- Platform-specific content adaptation

**Tools**:
```json
{
  "content_planner": {
    "description": "Create strategic content calendar",
    "parameters": {
      "timeframe": "object",
      "platforms": "array",
      "content_types": ["episode_promo", "behind_scenes", "tour_dates", "sponsor_content"],
      "posting_frequency": "object",
      "optimal_times": "object"
    }
  },
  "cross_platform_post": {
    "description": "Publish to multiple platforms simultaneously",
    "parameters": {
      "content": "object",
      "platforms": ["twitter", "instagram", "tiktok", "youtube", "linkedin"],
      "media_files": "array",
      "scheduling": "object",
      "platform_adaptation": "boolean"
    }
  },
  "community_engagement": {
    "description": "Manage audience interactions",
    "parameters": {
      "platform": "string",
      "engagement_type": ["comments", "dms", "mentions", "tags"],
      "response_style": ["professional", "casual", "humorous"],
      "auto_response_rules": "object",
      "escalation_threshold": "number"
    }
  },
  "performance_analytics": {
    "description": "Analyze content performance",
    "parameters": {
      "time_period": "string",
      "platforms": "array",
      "metrics": ["engagement", "reach", "conversion", "sentiment"],
      "content_type": "array",
      "comparison_period": "string"
    }
  },
  "viral_optimization": {
    "description": "Optimize content for virality",
    "parameters": {
      "content": "object",
      "platform": "string",
      "trending_topics": "array",
      "hashtag_strategy": "object",
      "posting_time": "string"
    }
  }
}
```

**Workflow**: `planning` → `creation` → `scheduling` → `engagement` → `analysis`

---

### 4. Content Distribution Agent
**Name**: `content_distributor`  
**Model**: `gpt-4o`  
**Role**: Website publishing and content delivery management

**Capabilities**:
- Website content publishing via Cloudflare
- SEO optimization and metadata management
- CDN performance optimization
- Podcast platform syndication
- Tour date and event management

**Tools**:
```json
{
  "website_publisher": {
    "description": "Publish content to website via Cloudflare",
    "parameters": {
      "content_type": ["episode", "blog_post", "tour_date", "announcement"],
      "content_data": "object",
      "seo_config": "object",
      "cdn_purge": "boolean",
      "cache_settings": "object"
    }
  },
  "tour_manager": {
    "description": "Manage tour dates and venue information",
    "parameters": {
      "tour_data": "array",
      "venues": "array",
      "ticket_links": "array",
      "promotion_settings": "object",
      "calendar_integration": "boolean"
    }
  },
  "syndication": {
    "description": "Distribute to podcast platforms",
    "parameters": {
      "episode_data": "object",
      "platforms": ["apple_podcasts", "spotify", "google_podcasts", "stitcher"],
      "rss_feed": "string",
      "embed_codes": "boolean"
    }
  },
  "seo_optimizer": {
    "description": "Optimize content for search engines",
    "parameters": {
      "content": "object",
      "target_keywords": "array",
      "meta_description": "string",
      "structured_data": "object",
      "image_alt_text": "array"
    }
  },
  "cdn_manager": {
    "description": "Manage Cloudflare CDN settings",
    "parameters": {
      "action": ["purge_cache", "update_settings", "analyze_performance"],
      "targets": "array",
      "optimization_level": ["basic", "standard", "aggressive"]
    }
  }
}
```

**Workflow**: `content_preparation` → `seo_optimization` → `publishing` → `distribution` → `performance_monitoring`

---

### 5. Sponsorship Management Agent
**Name**: `sponsorship_manager`  
**Model**: `gpt-4o`  
**Role**: Sponsor relationship management and content integration

**Capabilities**:
- Sponsor research and vetting
- Custom sponsor content creation
- Performance tracking and reporting
- Contract management support
- Revenue optimization

**Tools**:
```json
{
  "sponsor_research": {
    "description": "Identify and evaluate potential sponsors",
    "parameters": {
      "criteria": "object",
      "budget_range": "object",
      "excluded_categories": "array",
      "audience_alignment": "number",
      "brand_safety": "boolean"
    }
  },
  "content_creator": {
    "description": "Generate personalized sponsor content",
    "parameters": {
      "sponsor_info": "object",
      "integration_style": ["host_read", "produced_ad", "product_demo"],
      "duration": "number",
      "tone": ["professional", "casual", "enthusiastic"],
      "call_to_action": "string"
    }
  },
  "performance_tracker": {
    "description": "Monitor sponsor campaign effectiveness",
    "parameters": {
      "campaign_id": "string",
      "metrics": ["impressions", "clicks", "conversions", "brand_lift", "roi"],
      "time_period": "string",
      "attribution_model": "string"
    }
  },
  "report_generator": {
    "description": "Create comprehensive sponsor reports",
    "parameters": {
      "sponsor_id": "string",
      "report_period": "string",
      "include_demographics": "boolean",
      "format": ["pdf", "excel", "dashboard"],
      "executive_summary": "boolean"
    }
  },
  "revenue_optimizer": {
    "description": "Maximize sponsorship revenue",
    "parameters": {
      "inventory_analysis": "boolean",
      "pricing_strategy": "object",
      "package_deals": "array",
      "seasonal_adjustments": "object"
    }
  }
}
```

**Workflow**: `research` → `outreach` → `content_creation` → `tracking` → `reporting` → `optimization`

---

### 6. Tour & Events Management Agent
**Name**: `tour_manager`  
**Model**: `gpt-4o`  
**Role**: Live event coordination and tour promotion

**Capabilities**:
- Venue research and booking
- Tour itinerary management
- Ticket sales coordination
- Event promotion and marketing
- Travel and logistics planning

**Tools**:
```json
{
  "venue_scanner": {
    "description": "Find suitable venues for events",
    "parameters": {
      "location": "string",
      "capacity_range": "object",
      "budget_constraints": "number",
      "technical_requirements": "array",
      "date_range": "object",
      "venue_preferences": "array"
    }
  },
  "tour_scheduler": {
    "description": "Create optimal tour schedules",
    "parameters": {
      "cities": "array",
      "start_date": "string",
      "end_date": "string",
      "travel_time_optimization": "boolean",
      "back_to_back_events": "boolean",
      "rest_days": "array"
    }
  },
  "ticket_manager": {
    "description": "Handle ticket sales and inventory",
    "parameters": {
      "event_id": "string",
      "pricing_tiers": "object",
      "sales_platforms": "array",
      "inventory_limits": "object",
      "early_bird_pricing": "boolean"
    }
  },
  "event_promoter": {
    "description": "Promote events across channels",
    "parameters": {
      "event_details": "object",
      "promotion_channels": "array",
      "budget": "number",
      "target_audience": "array",
      "promotion_timeline": "object"
    }
  },
  "logistics_coordinator": {
    "description": "Manage travel and event logistics",
    "parameters": {
      "tour_schedule": "array",
      "travel_preferences": "object",
      "equipment_needs": "array",
      "accommodation_requirements": "object",
      "contingency_planning": "boolean"
    }
  }
}
```

**Workflow**: `planning` → `venue_booking` → `promotion` → `ticket_sales` → `logistics` → `execution`

---

## Integrated Workflows

### Complete Episode Production Pipeline
```json
{
  "name": "full_episode_production",
  "description": "From raw footage to distribution",
  "agents": ["video_editor", "audio_engineer", "social_media_manager", "content_distributor"],
  "steps": [
    {
      "step": 1,
      "agent": "video_editor",
      "action": "video_analysis",
      "input": "raw_footage",
      "output": "footage_analysis"
    },
    {
      "step": 2,
      "agent": "audio_engineer", 
      "action": "audio_cleanup",
      "input": "raw_audio",
      "output": "clean_audio"
    },
    {
      "step": 3,
      "agent": "video_editor",
      "action": "smart_cut",
      "input": "footage_analysis",
      "output": "edited_video"
    },
    {
      "step": 4,
      "agent": "sponsorship_manager",
      "action": "content_creator",
      "input": "sponsor_info",
      "output": "sponsor_content"
    },
    {
      "step": 5,
      "agent": "audio_engineer",
      "action": "sponsor_integration",
      "input": "clean_audio + sponsor_content",
      "output": "final_audio"
    },
    {
      "step": 6,
      "agent": "video_editor",
      "action": "create_short",
      "input": "edited_video",
      "output": "short_content"
    },
    {
      "step": 7,
      "agent": "content_distributor",
      "action": "website_publisher",
      "input": "final_episode_package",
      "output": "published_episode"
    },
    {
      "step": 8,
      "agent": "social_media_manager",
      "action": "cross_platform_post",
      "input": "short_content + episode_info",
      "output": "social_posts"
    }
  ]
}
```

### Tour Promotion Campaign
```json
{
  "name": "tour_promotion_campaign",
  "description": "Comprehensive tour marketing",
  "agents": ["tour_manager", "social_media_manager", "content_distributor"],
  "steps": [
    {
      "step": 1,
      "agent": "tour_manager",
      "action": "tour_scheduler",
      "input": "tour_requirements",
      "output": "tour_schedule"
    },
    {
      "step": 2,
      "agent": "content_distributor",
      "action": "tour_manager",
      "input": "tour_schedule",
      "output": "website_updates"
    },
    {
      "step": 3,
      "agent": "social_media_manager",
      "action": "content_planner",
      "input": "tour_info",
      "output": "promotion_calendar"
    },
    {
      "step": 4,
      "agent": "tour_manager",
      "action": "event_promoter",
      "input": "tour_schedule",
      "output": "campaign_content"
    },
    {
      "step": 5,
      "agent": "social_media_manager",
      "action": "cross_platform_post",
      "input": "campaign_content",
      "output": "live_promotions"
    }
  ]
}
```

---

## Agent Communication Protocols

### Inter-Agent Data Sharing
- **Video → Audio**: Timestamps for sponsor insertions
- **Audio → Social**: Audio clips for promotional content  
- **Social → Content**: Engagement metrics for optimization
- **Content → Tour**: Website traffic and conversion data
- **Sponsorship → All**: Integration requirements and restrictions

### Error Handling and Escalation
- **Tier 1**: Automatic retry with alternative parameters
- **Tier 2**: Human intervention required
- **Tier 3**: Critical failure - stop workflow and alert

### Quality Assurance
- **Content Review**: Automated brand safety and quality checks
- **Performance Monitoring**: Real-time tracking of key metrics
- **Feedback Loops**: Continuous improvement based on performance data

---

## Configuration Management

### Environment Variables
All agents support environment variable configuration for:
- API keys and tokens
- Model selection and parameters
- Rate limiting and throttling
- Logging and monitoring settings

### Scalability
- **Horizontal Scaling**: Multiple agent instances for high-volume workloads
- **Load Balancing**: Intelligent task distribution
- **Caching**: Response caching for improved performance

### Monitoring and Analytics
- **Performance Metrics**: Response times, success rates, error rates
- **Business Intelligence**: Content performance, ROI, audience growth
- **Resource Usage**: Compute costs, API usage, storage consumption