# Configuration Management

## Environment Configuration

### .env Template
```bash
# Podcast Production Environment Variables

# Podcast Identity
PODCAST_NAME="[PODCAST_NAME]"
HOST_NAME="[HOST_NAME]"
PODCAST_DESCRIPTION="[DESCRIPTION]"
TARGET_AUDIENCE="[AUDIENCE_DESCRIPTION]"

# Production Standards
AUDIO_SAMPLE_RATE="48000"
AUDIO_BIT_DEPTH="24"
AUDIO_TARGET_LUFS="-16"
AUDIO_TRUE_PEAK="-1.5"
VIDEO_RESOLUTION="4K"
VIDEO_MIN_RESOLUTION="1080p"
VIDEO_FRAME_RATE="60"

# Social Media Platform Tokens
TWITTER_BEARER_TOKEN="your_twitter_bearer_token"
INSTAGRAM_ACCESS_TOKEN="your_instagram_access_token"
TIKTOK_ACCESS_TOKEN="your_tiktok_access_token"
YOUTUBE_API_KEY="your_youtube_api_key"
LINKEDIN_ACCESS_TOKEN="your_linkedin_access_token"

# Cloudflare Configuration
CLOUDFLARE_API_KEY="your_cloudflare_api_key"
CLOUDFLARE_ACCOUNT_ID="your_cloudflare_account_id"
CLOUDFLARE_ZONE_ID="your_cloudflare_zone_id"
CLOUDFLARE_DNS_ID="your_cloudflare_dns_id"

# Security & Authentication
OPENAI_API_KEY="your_openai_api_key"
OPENAI_ORG_ID="your_openai_org_id"
BITWARDEN_CLIENT_ID="your_bitwarden_client_id"
BITWARDEN_CLIENT_SECRET="your_bitwarden_client_secret"

# Development & Testing
ENVIRONMENT="development"
LOG_LEVEL="info"
ENABLE_DEBUG_MODE="false"
TEST_MODE="false"

# Content Directories
RAW_FOOTAGE_DIR="raw_footage"
PRODUCTION_DIR="production"
SOCIAL_MEDIA_DIR="social_media"
TEMPLATES_DIR="templates"
OUTPUT_DIR="output"
```

## Agent Configuration

### agents_config.json Structure
```json
{
  "agents": {
    "core_production": {
      "name": "Core Production Agent",
      "model": "gpt-4o",
      "max_concurrent_tasks": 10,
      "response_timeout": 300,
      "quality_threshold": 0.95,
      "auto_escalation": true,
      "workflows": ["episode_production", "quality_control"]
    },
    "video_production": {
      "name": "Video Production Specialist",
      "model": "gpt-4o-vision-preview",
      "max_concurrent_tasks": 5,
      "response_timeout": 600,
      "speaker_detection_accuracy": 0.95,
      "output_formats": ["mp4", "mov", "webm"],
      "quality_standards": {
        "resolution_min": "1080p",
        "resolution_preferred": "4K",
        "frame_rate": "60",
        "codec": "h264"
      }
    },
    "audio_engineering": {
      "name": "Audio Engineering Specialist",
      "model": "gpt-4o",
      "max_concurrent_tasks": 3,
      "response_timeout": 900,
      "audio_standards": {
        "sample_rate": "48000",
        "bit_depth": "24",
        "target_lufs": "-16",
        "true_peak": "-1.5",
        "noise_floor": "-60"
      }
    },
    "social_media": {
      "name": "Social Media Manager",
      "model": "gpt-4o",
      "max_concurrent_tasks": 20,
      "response_timeout": 180,
      "platforms": ["twitter", "instagram", "tiktok", "youtube", "linkedin"],
      "posting_limits": {
        "daily_min": 3,
        "daily_max": 8,
        "weekly_min": 21
      },
      "response_times": {
        "mentions": "2_hours",
        "dms": "24_hours"
      }
    },
    "content_distribution": {
      "name": "Content Distribution Manager",
      "model": "gpt-4o",
      "max_concurrent_tasks": 15,
      "response_timeout": 300,
      "cdn_provider": "cloudflare",
      "publishing_standards": {
        "simultaneous_release_window": "30_minutes",
        "quality_check": true,
        "seo_optimization": true
      }
    },
    "sponsorship": {
      "name": "Sponsorship Manager",
      "model": "gpt-4o",
      "max_concurrent_tasks": 8,
      "response_timeout": 600,
      "sponsor_standards": {
        "max_runtime_percentage": 10,
        "min_roi": "3:1",
        "disclosure_required": true
      }
    },
    "tour_management": {
      "name": "Tour Management Specialist",
      "model": "gpt-4o",
      "max_concurrent_tasks": 6,
      "response_timeout": 900,
      "venue_standards": {
        "min_capacity": 500,
        "av_required": true,
        "backup_power": true
      }
    }
  },
  "workflows": {
    "episode_production": {
      "name": "Complete Episode Production",
      "agents": ["core_production", "video_production", "audio_engineering", "content_distribution"],
      "stages": ["recording", "editing", "processing", "distribution"],
      "quality_checkpoints": ["pre_recording", "post_recording", "pre_distribution"],
      "timeout_hours": 72
    },
    "social_media_campaign": {
      "name": "Social Media Campaign",
      "agents": ["social_media", "content_distribution"],
      "stages": ["planning", "creation", "scheduling", "engagement"],
      "quality_checkpoints": ["content_review", "timing_validation"],
      "timeout_hours": 48
    }
  }
}
```

## Platform-Specific Configurations

### Social Media Platform Settings
```json
{
  "platforms": {
    "twitter": {
      "api_version": "2",
      "character_limit": 280,
      "hashtag_limit": 3,
      "rate_limit": {
        "posts_per_hour": 30,
        "posts_per_day": 2400
      },
      "optimal_times": ["09:00-11:00", "13:00-15:00", "19:00-21:00"],
      "content_types": ["text", "image", "video"],
      "media_requirements": {
        "image": {"max_size": "5MB", "formats": ["jpg", "png", "webp"]},
        "video": {"max_size": "512MB", "max_duration": "140s", "formats": ["mp4", "mov"]}
      }
    },
    "instagram": {
      "api_version": "18.0",
      "hashtag_limit": 30,
      "rate_limit": {
        "posts_per_hour": 12,
        "stories_per_day": 100
      },
      "optimal_times": ["11:00-13:00", "19:00-21:00"],
      "content_mix": {
        "reels": 0.6,
        "posts": 0.25,
        "stories": 0.15
      },
      "media_requirements": {
        "photo": {"max_size": "30MB", "aspect_ratios": ["1:1", "4:5", "16:9"]},
        "video": {"max_size": "250MB", "max_duration": "90s", "aspect_ratios": ["16:9", "9:16"]}
      }
    },
    "tiktok": {
      "api_version": "open-api",
      "character_limit": 150,
      "hashtag_limit": 5,
      "rate_limit": {
        "posts_per_hour": 30
      },
      "optimal_times": ["19:00-21:00"],
      "content_requirements": {
        "video": {"min_duration": "15s", "max_duration": "180s", "aspect_ratio": "9:16"},
        "audio": {"require_trending": "true", "max_duration": "60s"}
      }
    },
    "youtube": {
      "api_version": "v3",
      "title_limit": 60,
      "description_limit": 5000,
      "tag_limit": 500,
      "rate_limit": {
        "uploads_per_day": 100
      },
      "optimal_times": ["14:00-16:00", "20:00-22:00"],
      "content_requirements": {
        "video": {"min_resolution": "720p", "preferred": "4K", "aspect_ratio": "16:9"},
        "thumbnail": {"resolution": "1280x720", "format": "jpg", "max_size": "2MB"}
      }
    },
    "linkedin": {
      "api_version": "v2",
      "character_limit": 3000,
      "rate_limit": {
        "posts_per_day": 100
      },
      "optimal_times": ["08:00-10:00", "12:00-13:00"],
      "content_requirements": {
        "text": {"min_length": 100, "max_length": 3000},
        "article": {"min_length": 500, "max_length": 100000},
        "image": {"max_size": "10MB", "formats": ["jpg", "png", "gif"]}
      }
    }
  }
}
```

## Quality Control Configuration

### Quality Standards Validation
```json
{
  "quality_control": {
    "audio": {
      "sample_rate_min": "48000",
      "bit_depth_min": "24",
      "target_lufs": "-16",
      "true_peak_max": "-1.5",
      "noise_floor_max": "-60",
      "frequency_range": "20Hz-20kHz",
      "dynamic_range_min": "60dB"
    },
    "video": {
      "resolution_min": "1920x1080",
      "resolution_preferred": "3840x2160",
      "frame_rate_min": "30",
      "frame_rate_preferred": "60",
      "codec": "h264",
      "bitrate_min": "8Mbps",
      "bitrate_preferred": "50Mbps",
      "color_space": "Rec.709",
      "color_depth": "8-bit"
    },
    "content": {
      "accuracy_threshold": 0.99,
      "brand_compliance": true,
      "legal_compliance": true,
      "accessibility_compliance": true,
      "fact_checking_required": true
    },
    "performance": {
      "min_engagement_rate": 0.03,
      "min_completion_rate": 0.70,
      "min_share_rate": 0.02,
      "min_growth_rate": 0.05,
      "max_error_rate": 0.01
    }
  }
}
```

## Security Configuration

### Security Settings
```json
{
  "security": {
    "data_protection": {
      "encryption_algorithm": "AES-256",
      "key_rotation_days": 90,
      "backup_encryption": true,
      "transmission_encryption": true
    },
    "access_control": {
      "authentication_required": true,
      "two_factor_required": true,
      "session_timeout": "8h",
      "role_based_access": true
    },
    "network_security": {
      "firewall_enabled": true,
      "vpn_required": true,
      "intrusion_detection": true,
      "ssl_tls_min_version": "1.2"
    },
    "audit_logging": {
      "enabled": true,
      "log_retention_days": 365,
      "failed_login_alerts": true,
      "data_access_logging": true
    }
  }
}
```

## Backup & Recovery Configuration

### Backup Strategy Settings
```json
{
  "backup_strategy": {
    "three_two_one_rule": {
      "total_copies": 3,
      "media_types": 2,
      "offsite_copies": 1
    },
    "storage_locations": {
      "primary": {
        "type": "local_ssd",
        "capacity": "50TB",
        "raid_level": 10
      },
      "secondary": {
        "type": "local_hdd",
        "capacity": "100TB",
        "raid_level": 6
      },
      "offsite": {
        "type": "cloud_storage",
        "provider": "aws_s3",
        "encryption": true,
        "versioning": true
      }
    },
    "backup_schedule": {
      "incremental": "6_hours",
      "full_backup": "daily",
      "verification": "weekly",
      "retention": {
        "raw_footage": "90_days",
        "final_content": "indefinite",
        "archived_projects": "7_years"
      }
    },
    "disaster_recovery": {
      "rto": "4_hours",  # Recovery Time Objective
      "rpo": "1_hour",   # Recovery Point Objective
      "test_frequency": "quarterly",
      "documentation_required": true
    }
  }
}
```

## Performance Monitoring

### Monitoring Configuration
```json
{
  "monitoring": {
    "system_health": {
      "cpu_threshold": "80%",
      "memory_threshold": "85%",
      "disk_threshold": "90%",
      "network_threshold": "100Mbps",
      "check_interval": "60_seconds"
    },
    "application_performance": {
      "response_time_threshold": "5_seconds",
      "error_rate_threshold": "1%",
      "uptime_target": "99.9%",
      "alert_channels": ["slack", "email", "sms"]
    },
    "content_performance": {
      "engagement_threshold": "3%",
      "completion_threshold": "70%",
      "quality_score_threshold": "95%",
      "growth_threshold": "5%",
      "reporting_frequency": "weekly"
    },
    "alerting": {
      "critical_issues": ["immediate", "sms", "call"],
      "major_issues": ["immediate", "slack", "email"],
      "minor_issues": ["hourly", "slack"],
      "performance_issues": ["daily", "email"]
    }
  }
}
```

---

## Configuration Management Guidelines

### File Organization
- Place all configuration files in `config/` directory
- Use version control for all non-sensitive configurations
- Encrypt sensitive configurations and use environment variables
- Maintain separate configurations for different environments

### Update Procedures
1. **Test Changes**: Always test in development environment first
2. **Document Changes**: Update documentation for all configuration changes
3. **Version Control**: Commit configuration changes with clear messages
4. **Rollback Plan**: Maintain previous configuration versions
5. **Notify Team**: Alert relevant team members of changes

### Security Best Practices
- Never commit sensitive data to version control
- Use environment variables for all API keys and tokens
- Implement role-based access for configuration changes
- Regular security audits of configuration files
- Encryption for sensitive configuration storage

### Maintenance Schedule
- **Weekly**: Review performance metrics and adjust as needed
- **Monthly**: Review security configurations and update credentials
- **Quarterly**: Full configuration audit and cleanup
- **Annually**: Complete configuration review and optimization