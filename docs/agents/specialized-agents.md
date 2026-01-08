# Specialized Production Agents

## Video Production Specialist

### Role Definition
Expert in video editing, camera operation, and visual storytelling with AI-powered automation capabilities.

### Core Responsibilities
- **Multi-Camera Editing**: AI-driven speaker detection and automatic angle switching
- **Color Grading**: Professional color correction and visual enhancement
- **Short-Form Content**: Platform-specific video optimization
- **Visual Effects**: Motion graphics, overlays, and branding elements

### Technical Capabilities
- **Camera Angle Automation**: 95% accuracy on speaker detection
- **Format Optimization**: Platform-specific video formatting
- **Quality Enhancement**: AI-powered upscaling and restoration
- **Brand Consistency**: Automated lower thirds and logo placement

### Tools Integration
```json
{
  "video_analysis": "AI-powered content analysis",
  "smart_cutting": "Automated camera angle selection",
  "color_grading": "Professional color correction",
  "format_optimization": "Multi-platform output formatting"
}
```

## Audio Engineering Specialist

### Role Definition
Professional audio engineer specializing in podcast production with advanced processing and mastering capabilities.

### Core Responsibilities
- **Audio Cleanup**: Noise reduction, de-essing, and audio restoration
- **Voice Enhancement**: EQ, compression, and vocal processing
- **Sponsor Integration**: Seamless commercial content insertion
- **Mastering**: Platform-specific audio optimization

### Technical Capabilities
- **Noise Reduction**: -60dB noise floor achievement
- **Loudness Normalization**: -16 LUFS target with True Peak control
- **Multi-Track Processing**: Independent processing for each speaker
- **Real-Time Processing**: Live audio monitoring and adjustment

### Tools Integration
```json
{
  "audio_cleanup": "Advanced noise and artifact removal",
  "voice_enhancement": "Professional vocal processing",
  "sponsor_integration": "Seamless commercial insertion",
  "mastering": "Platform-specific audio optimization"
}
```

## Social Media Management Specialist

### Role Definition
Multi-platform social media expert with automated content creation, scheduling, and engagement management.

### Core Responsibilities
- **Content Creation**: Platform-specific content generation and adaptation
- **Scheduling**: Advanced posting schedules and optimization
- **Community Management**: Engagement monitoring and response automation
- **Analytics**: Performance tracking and optimization strategies

### Technical Capabilities
- **Cross-Platform Posting**: Simultaneous multi-platform content distribution
- **Automated Engagement**: AI-powered comment and mention responses
- **Performance Optimization**: Real-time content performance analysis
- **Trend Integration**: Automated trending topic integration

### Tools Integration
```json
{
  "content_creation": "AI-powered content generation",
  "cross_posting": "Multi-platform content distribution",
  "engagement_automation": "Automated response management",
  "analytics_optimization": "Performance-driven content strategy"
}
```

## Thumbnail Agent

### Role Definition
Generates a thumbnail brief and AI prompt using title, summary, transcript, and keyframes.

### Core Responsibilities
- **Brief Generation**: Extract hook and keyword suggestions.
- **Style Guidance**: Provide text overlay and composition notes.
- **Asset Output**: Emit a JSON brief for design or AI tools.

### Tools Integration
```json
{
  "thumbnail_brief": "Prompt + layout suggestions",
  "keyframe_selection": "Optional keyframe hints"
}
```

## SEO Agent

### Role Definition
Builds SEO metadata and JSON-LD schema for episode pages.

### Core Responsibilities
- **Metadata Packaging**: Titles, descriptions, and keywords.
- **Schema Generation**: JSON-LD for PodcastEpisode.
- **Validation**: Ensure canonical URLs and image links.

### Tools Integration
```json
{
  "jsonld_builder": "PodcastEpisode schema generator",
  "metadata_pack": "SEO-ready JSON bundle"
}
```

## Social Scheduler Agent

### Role Definition
Creates platform schedules and triggers publishing workflows with offsets.

### Core Responsibilities
- **Schedule Planning**: Base time + platform offsets.
- **Publish Routing**: Call API/MCP publish flow.
- **Validation**: Verify scheduled posts.

### Tools Integration
```json
{
  "schedule_builder": "Offset-based scheduling",
  "workflow_runner": "Social publish integration"
}
```

## Archive Agent

### Role Definition
Builds archive manifests and uploads media to R2/B2 storage.

### Core Responsibilities
- **Manifest Creation**: File lists with hashes.
- **Upload Coordination**: S3-compatible transfers.
- **Integrity Checks**: Hash validation for restores.

### Tools Integration
```json
{
  "archive_manifest": "File inventory + hashes",
  "s3_upload": "R2/B2 compatible upload"
}
```

## Troubleshooting Agent

### Role Definition
Runs diagnostics, config validation, and targeted tests to identify failures quickly.

### Core Responsibilities
- **Config Validation**: JSON/TOML parsing checks.
- **Credential Audits**: Offline/live token checks.
- **Diagnostics**: Stream endpoints, disk, and network health snapshots.
- **Log Scanning**: Surface warnings and error patterns.

### Tools Integration
```json
{
  "config_checks": "Validate config files",
  "diagnostics": "Run system snapshot",
  "pytest": "Targeted test execution"
}
```

## Content Distribution Specialist

### Role Definition
Web and content distribution expert managing website publishing, CDN optimization, and platform syndication.

### Core Responsibilities
- **Website Publishing**: Content management and publication automation
- **CDN Management**: Content delivery optimization and caching
- **Platform Syndication**: Podcast platform distribution and management
- **SEO Optimization**: Search engine optimization and metadata management

### Technical Capabilities
- **Automated Publishing**: Content publication workflow automation
- **Performance Optimization**: CDN optimization and speed enhancement
- **SEO Management**: Automated SEO optimization and monitoring
- **Analytics Integration**: Performance tracking and reporting

### Tools Integration
```json
{
  "website_publishing": "Automated content management",
  "cdn_optimization": "Performance and caching management",
  "syndication": "Multi-platform content distribution",
  "seo_optimization": "Search engine optimization"
}
```

## Sponsorship Management Specialist

### Role Definition
Business development and sponsorship expert managing sponsor relationships, content creation, and performance tracking.

### Core Responsibilities
- **Sponsor Acquisition**: New sponsor research and relationship building
- **Content Creation**: Custom sponsor content generation and integration
- **Performance Tracking**: ROI analysis and performance reporting
- **Contract Management**: Sponsor agreement management and compliance

## Live Director Agent

### Role Definition
Automates live scene switching based on audio activity to keep the camera on the active speaker.

### Core Responsibilities
- **Speaker Detection**: Monitor per-mic audio levels.
- **Scene Switching**: Trigger OBS scene changes with cooldown control.
- **Override Handling**: Allow manual override for host or emergency scenes.

### Tools Integration
```json
{
  "obs_websocket": "Scene switching control",
  "audio_metering": "Active speaker detection",
  "cooldown": "Prevent rapid scene changes"
}
```

## Assistant Orchestrator

### Role Definition
Central assistant that summarizes system status and routes tasks to agents.

### Core Responsibilities
- **Status Reporting**: Surface configs, SOPs, and open tasks.
- **Credential Health**: Run offline checks and optional live checks.
- **Workflow Routing**: Delegate tasks to agents and scripts.

### Technical Capabilities
- **Automated Prospecting**: AI-powered sponsor identification and vetting
- **Custom Content Generation**: Brand-aligned sponsor content creation
- **Performance Analytics**: Real-time ROI tracking and optimization
- **Compliance Monitoring**: Automated contract compliance checking

### Tools Integration
```json
{
  "prospect_research": "AI-powered sponsor identification",
  "content_creation": "Custom sponsor content generation",
  "performance_tracking": "Real-time ROI and analytics",
  "compliance_management": "Contract and compliance monitoring"
}
```

## Tour Management Specialist

### Role Definition
Event coordination and tour management expert handling venue booking, logistics, and event promotion.

### Core Responsibilities
- **Venue Management**: Venue research, booking, and coordination
- **Logistics Coordination**: Travel, equipment, and event logistics
- **Event Promotion**: Tour marketing and ticket sales management
- **Fan Experience**: VIP management and fan engagement

### Technical Capabilities
- **Automated Booking**: AI-powered venue identification and booking
- **Logistics Optimization**: Travel and equipment scheduling optimization
- **Promotion Automation**: Multi-platform tour marketing automation
- **Experience Management**: VIP and fan experience coordination

### Tools Integration
```json
{
  "venue_booking": "Automated venue identification and booking",
  "logistics_coordination": "Travel and equipment optimization",
  "promotion_automation": "Multi-platform tour marketing",
  "experience_management": "VIP and fan experience coordination"
}
```

---

## Agent Integration Architecture

### Inter-Agent Communication
- **Production Pipeline**: Sequential handoffs with quality checkpoints
- **Data Sharing**: Real-time data exchange between agents
- **Conflict Resolution**: Automated conflict detection and resolution
- **Performance Monitoring**: Cross-agent performance tracking

### Workflow Orchestration
- **Task Assignment**: Intelligent task distribution based on agent capabilities
- **Load Balancing**: Workload distribution across agent pool
- **Dependency Management**: Task dependency tracking and scheduling
- **Quality Assurance**: Multi-agent quality validation

### Error Handling and Recovery
- **Failover Systems**: Automatic agent failover and recovery
- **Error Detection**: Real-time error identification and reporting
- **Recovery Procedures**: Automated recovery and manual intervention points
- **Learning Systems**: Error pattern recognition and prevention

---

## Agent Performance Standards

### Quality Metrics
- **Task Completion Rate**: 98%+ successful task completion
- **Accuracy Rate**: 95%+ accuracy in core tasks
- **Response Time**: 5-minute maximum response time
- **Error Rate**: <2% error rate in all operations

### Efficiency Metrics
- **Task Throughput**: Minimum 10 tasks/hour per agent
- **Resource Utilization**: 80%+ efficient resource usage
- **Processing Time**: 95% of tasks completed within SLA
- **Scalability**: Handle 10x load without performance degradation

### Learning and Improvement
- **Adaptation Rate**: Continuous performance improvement
- **Skill Development**: Ongoing capability enhancement
- **Feedback Integration**: 90%+ feedback implementation rate
- **Innovation**: Regular feature and capability additions
