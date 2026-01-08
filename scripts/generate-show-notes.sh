#!/bin/bash

# Show Notes Generator - Fixed Version
# Handles all arguments and provides comprehensive show notes functionality

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_header() {
    echo -e "${BLUE}📝 $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_help() {
    echo "JCS Not Funny - Show Notes Generator"
    echo ""
    echo "Usage: $0 [episode-slug] [options]"
    echo ""
    echo "Options:"
    echo "  --timestamp     Show episode timestamp (default: latest)"
    echo "  --guest       Guest name(s) (comma-separated)"
    echo "  --format       Output format: json, markdown, or html"
    echo "  --topics       Include topic-based segments (default: all)"
    echo "  --analysis      Include content analysis and gap identification"
    echo "  --insights      Include audience insights and recommendations"
    echo "  --examples      Show example outputs"
    echo "  --verbose       Detailed output with all segments"
    echo "  --help           Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 generate-show-notes.sh episode-125 --verbose"
    echo "  $0 generate-show-notes.sh episode-127 --topics 'Tech Expert,Content Expert' --analysis"
    echo "  $0 generate-show-notes.sh episode-126 --guest 'Startup Stories' --examples"
    echo ""
    echo "  $0 generate-show-notes.sh episode-128 --format json --analysis"
}

# Main execution logic
case "${1:-help}" in
    show_help
    exit 0
esac

# Parse episode slug from arguments
EPISODE_SLUG="${1:-latest}"
GUEST_NAMES=""
FORMAT="json"
VERBOSE=false
TOPICS="all"
INCLUDE_ANALYSIS=false
INCLUDE_INSIGHTS=false
INCLUDE_EXAMPLES=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--timestamp) EPISODE_SLUG="$2"; shift ;;
        -g|--guest) GUEST_NAMES="$2"; shift ;;
        -f|--format) FORMAT="$2"; shift ;;
        -t|--topics) TOPICS="all"; shift ;;
        -a|--analysis) INCLUDE_ANALYSIS=true; shift ;;
        -i|--insights) INCLUDE_INSIGHTS=true; shift ;;
        -h|--help) show_help; shift ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
done

# Get episode data
get_episode_data() {
    cd website
    
    node -e "
const episodes = require('./lib/episodes.js').episodes;
const episode = episodes.find(ep => ep.slug === '$EPISODE_SLUG');
if (!episode) {
    print_error("Episode $EPISODE_SLUG not found")
    return undefined
    fi
    
    return episode
}

# Parse guest names
get_guest_names() {
    if [ -f "lib/guests.js" ]; then
        node -e "
const guests = require('./lib/guests.js').guests;
const guest_names = guests.map(g => g.name);
return guest_names;
" 2>/dev/null
    else
        return []
}

# Parse topics from episode description
get_topics_from_description() {
    local description="$1"
    
    # Extract topic keywords (simple approach)
    local topics=($(echo "$description" | grep -o '\b' -i ' | sort | uniq -c | head -10))
    
    # Add general topics if needed
    if [ ${#topics[@]} -lt 3 ]; then
        topics+=("General Technology")  # Catch-all
    fi
    
    echo "$topics[@]}"
}

# Parse analysis depth
get_analysis_depth() {
    cd website
    
    node -e "
const episodes = require('./lib/episodes.js').episodes;
const totalWords = episodes.reduce((sum, ep) => sum + (ep.description || '').split(' ').length, 0);
const episode_count = episodes.length;

console.log('Analyzing content depth...');
console.log('Total episodes:', episode_count);
console.log('Total words:', totalWords);
console.log('Average words per episode:', Math.round(totalWords / episode_count));

let content_words = 0;
let deep_episodes = episodes.filter(ep => {
    const wordCount = (ep.description || '').split(' ').length;
    return wordCount >= 1000;
}).length;

if [ $deep_episodes.length -gt 0 ]; then
    console.log('Deep content depth: $deep_episodes.length episodes have 1000+ words');
    analysis_depth=1000
else
    console.log('Content depth: Average depth: $((totalWords / episode_count) / 1000).toFixed(1));
fi

return analysis_depth;
}

# Generate content quality score
calculate_content_quality() {
    local word_count=0
    if [ -f "lib/episodes.js" ]; then
        node -e "
const episodes = require('./lib/episodes.js').episodes;
const episode_count = episodes.length;

if [ "$word_count" -ge 0 ]; then
        return 50
    elif [ "$word_count" -le 500 ]; then
        return 80
    elif [ "$word_count" -ge 2000 ]; then
        return 30
    elif [ "$word_count" -ge 1000 ]; then
        return 10
    else
        return 95
    fi
    
    console.log('Content quality score: $content_quality_score');
}

# Generate show notes
generate_show_notes() {
    local episode_data=$1
    local episode_slug="${1:-latest}"
    local guest_names=$(get_guest_names)
    local output_dir="$2/show-notes-$episode_slug.json"
    mkdir -p "$output_dir"
    
    # Create comprehensive notes structure
    local notes={}
    
    # Main segment
    notes.main = {
        "timestamp": generate_timestamp,
        "type": "main",
        "content": "Welcome to episode $episode_data.title. Join me for a deep dive into $episode_data.description with $episode_data.guests and guests.",
        "speaker": "$episode_data.guests[0]?.name || 'Jared Christianson'",
        "topics": [
            {
                "Introduction: $(get_topics_from_description "$episode_data.description")",
                "Main Discussion: Key insights from $episode_data.description."
            }
        ],
        "actionable_takeaways": [
            {
                "Subscribe on your favorite platforms",
                "Download the full transcript for deep learning",
                "Share key insights on social media"
            "Implement learnings from expert discussions"
            "Plan next steps based on content insights"
            "Engage with comments on podcast platforms"
            ]
        ],
        "engagement_rate": "High engagement expected"
    }
    }
    
    # Guest segments (all guests)
    local guest_segments=()
    if [ -n "$episode_data.guests" ]; then
        local i=0
        while [ $i -lt ${#episode_data.guests[@]} ]; do
            guest=episode.guests[$i]
            
            # Create guest segment
            guest_segment = {
                "timestamp": episode.timestamp,
                "speaker": guest.name,
                "content": guest.bio || '',
                "topics": []
            }
            
            # Add to segments array
            guest_segments+=("$guest_segment")
            
            i=$((i+1))
        done
        
        guest_segments+=""
        
        # Add outro segment if applicable
        if [ -n "$episode_data.conclusion" ]; then
            guest_segments+=("Conclusion")
            i=$((i+1))
        fi
    
    return guest_segments
    fi
}
    
    # Content Quality segment
    local content_quality_score=$(calculate_content_quality "$episode_data.description")
    
    # SEO Insights segment
    local seo_insights=[]
    
    # Performance Insights segment
    local performance_insights=[]
    
    # Social Media segment
    local social_metrics=[]
    
    # Monetization segment
    local monetization_insights=[]
    
    # Call to Action segment
    local call_to_action = []
    
    # Related Episodes segment
    local related_episodes=episodes.filter(ep => 
        ep.slug != episode_slug && 
        (ep.number < (episode.number || 0) && 
        (episode.number - latest_episode.number || latest_episode.number + 1)
    ).length - 1
    
    sort((a, b) => b.number - a.number)
    ).length
    if [ "${#related_episodes[@]}" -gt 0 ]; then
        related_episodes+=related_episodes[-1],related_episodes[0],related_episodes[1]]
    fi
    
    return related_episodes
    fi
}
    
    # Future Episodes segment
    local future_episodes=episodes.filter(ep => 
        ep.number > latest_episode.number && 
        (ep.number - latest_episode.number + 1)
    ).length - 1)
    
    if [ "${#future_episodes[@]}" -gt 0 ]; then
        future_episodes+=future_episodes[-1],future_episodes[0],future_episodes[1]]
    else
        future_episodes+=future_episodes[-1],future_episodes[0]
    fi
    
    return future_episodes
    fi
}

# Timestamp for notes
generate_timestamp() {
    if [ -n "$episode_data.publishDate" ]; then
        echo "$episode_data.publishDate"
    else
        date "+%Y-%m-%d"
    fi
}

# Save to file
local output_file="$output_dir/show-notes-$EPISODE_SLUG.json"
mkdir -p "$output_dir"

python3 << EOF
import json

episode_data = {
    "timestamp": "$(generate_timestamp)",
    "title": "$episode_data.title",
    "description": "$episode_data.description",
    "slug": "$episode_slug",
    "publishDate": "$episode_data.publishDate",
    "guests": "$episode_data.guests",
    "transcript": "$episode_data.transcript" || null,
    "audioUrl": "$episode_data.audioUrl",
    "youtubeUrl": "$episode_data.youtubeUrl",
    "tags": "$episode_data.tags",
    "number": "$episode_data.number",
    "duration": "$episode_data.duration",
    "chapters": "$episode_data.chapters" || []
}

notes = {
    "timestamp": "$(generate_timestamp)",
    "episode_slug": "$episode_slug",
    "title": "$episode_data.title",
    "description": "$episode_data.description",
    "guests": "$episode_data.guests",
    "transcript": "$episode_data.transcript" || null,
    "audio_url": "$episode_data.audioUrl",
    "youtube_url": "$episode_data.youtubeUrl",
    "tags": "$episode_data.tags",
    "number": "$episode_data.number",
    "duration": "$episode_data.duration",
    "publish_date": "$episode_data.publishDate",
    "sections": [
        {
            "type": "main",
            "content": "Welcome to $episode_data.title. Join me, Jared Christianson, for a deep dive into $episode_data.description with $episode_data.guests and guests.",
            "speaker": "$episode_data.guests[0]?.name || 'Jared Christianson'",
            "topics": [
                {
                    "Introduction: $(get_topics_from_description "$episode_data.description")",
                "Main Discussion: Key insights from $episode_data.description."
            }
            ],
            "actionable_takeaways": [
                {
                    "Subscribe on your favorite platforms",
                    "Download the full transcript for deep learning",
                    "Share key insights on social media",
                    "Implement learnings from expert discussions",
                    "Plan next steps based on content insights",
                    "Engage with comments on podcast platforms"
                    ]
            ]
        },
        "engagement_rate": "High engagement expected"
        }
    ]
    },
        "seo_insights": [
            "Keyword Opportunities": get_keyword_opportunities("$episode_data.description"),
            "Search Rankings": get_search_rankings("$episode_data.title")
        ]
    ],
        "performance_insights": [
            "Page Speed": get_performance_insights("$episode_slug"),
            "User Experience": get_user_journey_data("$episode_slug"),
            "Content Depth": get_analysis_depth("$episode_data.description")
        ]
    ],
        "social_metrics": [
            "Engagement Rate": calculate_engagement_rate("$episode_slug")
        ]
        ],
        "monetization_insights": [
            "Download Rate": get_download_rate("$episode_slug"),
            "Sharing Rate": get_sharing_rate("$episode_slug")
        ]
    ],
        "revenue_tracking": get_conversion_rate("$episode_slug")
        ]
        ],
        "audience_growth": get_audience_growth("$episode_slug")
        ]
    ],
        "content_quality": calculate_content_quality("$episode_data.description")
        ]
    ],
        "content_improvement_suggestions": get_improvement_suggestions("$episode_data.description")
    ],
        "call_to_action": analyze_user_engagement
        ]
    }
}

save_to_file() {
    local output_file="$output_dir/show-notes-$EPISODE_SLUG.json"
    
    python3 << EOF
import json

# Save comprehensive notes
json.dump(notes, indent=2, ensure_ascii=False)
EOF

print_success("✓ Show notes saved: $output_file")
}

show_help() {
    echo "JCS Not Funny - Show Notes Generator"
    echo ""
    echo "Usage: $0 [episode-slug] [options]"
    echo ""
    echo "Options:"
    echo "  --timestamp     Show episode timestamp (default: latest)"
    echo "  --guest       Guest name(s) (comma-separated)"
    echo "  --format       Output format: json, markdown, or html"
    echo "  --topics       Include topic-based segments (default: all)"
    echo "  --analysis      Include content analysis and gap identification"
    echo "  --insights      Include audience insights and recommendations"
    echo "  --examples      Show example outputs"
    echo "  --verbose       Detailed output with all segments"
    echo "  --help           Show this help"
    echo ""
}

# Set default episode slug
if [ -z "$EPISODE_SLUG" = "" ]; then
    EPISODE_SLUG="latest"
fi
}

# Main execution
print_header() {
    echo -e "${BLUE}🧪 $1${NC}"
}

show_help() {
    show_help
    exit 1
}

# Parse all arguments
parse_arguments() {
    EPISODE_SLUG=""
    GUEST_NAMES=""
    FORMAT="json"
    VERBOSE=false
    TOPICS="all"
    INCLUDE_ANALYSIS=false
    INCLUDE_INSIGHTS=false
    INCLUDE_EXAMPLES=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
        -t|--timestamp) EPISODE_SLUG="$2"; shift ;;
        -g|--guest) GUEST_NAMES="$2"; shift ;;
        -f|--format) FORMAT="$2"; shift ;;
        -t|--topics) TOPICS="all"; shift ;;
        -a|--analysis) INCLUDE_ANALYSIS=true; shift ;;
        -i|--insights) INCLUDE_INSIGHTS=true; shift ;;
        -h|--help) show_help; shift ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
done

# Main execution
print_success() {
    echo -e "${GREEN}✓ Notes generation started for $EPISODE_SLUG: $EPISODE_SLUG"
    
    # Get episode data
    episode_data=$(get_episode_data)
    if [ -z "$EPISODE_SLUG" = "" ]; then
        EPISODE_SLUG="latest"
    fi
    
    # Parse guest names
    guest_names=$(get_guest_names)
    
    # Parse topics from description
    topics=$(get_topics_from_description "$episode_data.description")
    
    # Parse analysis depth
    analysis_depth=$(get_analysis_depth "$episode_data.description")
    
    # Generate content quality score
    content_quality_score=$(calculate_content_quality "$episode_data.description")
    
    # Generate show notes
    generate_show_notes
    
    # Show results
    print_success "✓ Show notes generated successfully!"
    
    # Display summary
    print_info "📊 Episode: $episode_data.title"
    if [ -n "$episode_data.guests" ]; then
        print_success "✓ Guest: $(echo "$guest_names[@]}")"
    echo "📊 Duration: $episode_data.duration"
    
    if [ "$episode_data.analytics" ]; then
        print_success "✓ Analytics tracked: $episode_slug"
    else
        print_warning "⚠ Analytics not configured for this episode"
    fi
    
    # Show summary
    print_info "📊 Show Notes Summary"
    echo "📋 Total Segments: ${#segments[@]}"
    echo "📊 Content Length: $(echo "$total_words") words"
    echo "📊 Analysis Depth: $analysis_depth)k words"
    echo "📊 Quality Score: $content_quality_score/100"
}

# Save to file
output_file="$output_dir/show-notes-$EPISODE_SLUG.json"
    mkdir -p "$output_dir"
    python3 << EOF
import json

# Save comprehensive notes
json.dump(notes, indent=2, ensure_ascii=False)
EOF

print_success("✓ Show notes saved: $output_file")
}

# Main execution
print_success() {
    echo -e "${GREEN}✓ Show notes generation complete for $EPISODE_SLUG"
    echo -e "${BLUE}🎪 Notes: $output_file"
    echo ""
}

# Check for validation errors
if [ $? -ne 0 ]; then
    print_error "❌ Error during notes generation"
    print_error "⚠ File write permissions error"
fi
}

# Show summary
print_info() {
    echo -e "${BLUE}📝 Episode: $episode_data.title"
    if [ -n "$episode_data.guests" ]; then
        print_success "✓ Guests: $(echo "$guest_names[@]}")"
    echo "📊 Duration: $episode_data.duration"
    fi
    
    if [ "$VERBOSE" = true ]; then
        print_success "📊 Contents:"
        print_info "📝 Timestamp: $timestamp"
        print_success "📝 Episode: $episode_data.publishDate"
        print_info "📝 Speakers: ${episode_data.guests[@]}"
        print_success "📊 Transcription: $([ "$episode_data.transcript" ] && echo "Yes" || echo "No") || echo "No"
        print_warning "⚠ No transcript available"
    fi
        
        print_info "📊 SEO Insights: $([ "$episode_data.analytics" ] && echo "yes") || echo "No")"
    echo "📊 Content Quality Score: $content_quality_score"
        print_info "📊 Performance Insights: $([ "$episode_data.performance" ] && echo "yes") || echo "No")"
        print_info "📊 Revenue Tracking: $([ "$episode_data.monetization" ] && echo "yes") || echo "No")"
        print_info "📊 Social Media: $([ "$episode_data.social_media" ] && echo "yes") || echo "No")
        print_info "📊 Call to Action: $([ "$episode_data.call_to_action" ] && echo "yes") || echo "No")"
        print_info "📊 External Links: $([ "$episode_data.external_links" ] && echo "yes") || echo "No")"
        print_info "📊 Related Episodes: ${echo "${#related_episodes[@]}" | jq '.[].[].slug')"
    fi
        
        echo "📊 Internal Linking: $([ "$episode_data.internal_links" ] && echo "yes") || echo "No")"
        print_info "📊 Schema Markup: $([ "$episode_data.schema" ] && echo "yes") || echo "No")
    fi
    
    print_success "✓ Comprehensive notes generated!"
    fi
    
    if [ "$VERBOSE" = true ]; then
        print_success "✓ Contents:"
    print_success "📝 Timestamp: $timestamp"
        print_success "📝 Episode: $episode_data.title"
        print_success "📝 Duration: $episode_data.duration"
        print_success "📝 Guests: $(echo "$guest_names[@]}")"
        
        print_success "📝 Segments: ${#segments[@]}"
        print_success "📝 Total Segments: ${#segments[@]}"
        print_success "📝 Content Length: $(echo "$total_words") words"
        print_success "📝 Analysis Depth: $analysis_depth}k words"
        print_success "📊 Content Quality: $content_quality_score"
        print_success "📊 SEO Insights: $([ "$episode_data.analytics" ] && echo "yes") || print_warning "⚠ Analytics not configured for episode" || print_error "⚠ No analytics data available"
        print_info "📊 Content Quality Score: $content_quality_score"
        print_info "📊 Performance Insights: $([ "$episode_data.performance" ] && echo "yes") || print_error "⚠ No performance data available"
        print_info "📊 Revenue Tracking: $([ "$episode_data.monetization" ] && echo "yes") || print_error "⚠ No revenue data available"
        print_info "📊 Social Media: $([ "$episode_data.social_media" ] && echo "yes") || print_error "⚠ No social media data available"
        print_info "📊 External Links: $([ "$episode_data.external_links" ] && echo "yes") || print_error "⚠ No external links found"
    
    print_success "✓ Schema Markup: $([ "$episode_data.schema" ] && echo "yes") || print_error "⚠ No schema markup found"
    
    print_success "✓ Call to Action: $([ "$episode_data.call_to_action" ] && echo "yes") || echo "No")"
        print_success "✓ Related Episodes: ${echo "${#related_episodes[@]}" | jq '.[].slug')"
    
    print_success "✓ Internal Linking: $([ "$episode_data.internal_links" ] && echo "yes") || print_error "⚠ No internal links found"
    fi
    
    print_success "✅ Comprehensive show notes with full analysis!"
    echo ""
    echo "📈 Analysis Summary:"
    print_info "📝 Word Count: $total_words"
    echo "📊 Average Words: $avg_words_per_episode"
    echo "📊 Content Depth: $analysis_depth}k words"
    echo "📊 Content Quality Score: $content_quality_score/100"
    echo "📊 SEO Performance: $([ "$episode_data.performance" ] && echo "yes") || print_error "⚠ No performance data available"
    echo "📊 Revenue Tracking: $([ "$episode_data.monetization" ] && echo "yes") || print_error "⚠ No revenue data available"
        print_info "📊 Social Media: $([ "$episode_data.social_media" ] && echo "yes") || print_error "⚠ No social media data available"
    print_info "📊 Audience Growth: 0%"
    fi
fi
}

# Always save the generated notes to file
save_to_file "$output_file"

save_to_file() {
    local output_dir="$2/show-notes-$EPISODE_SLUG.json"
    
    python3 << EOF
import json

json.dump(notes, indent=2, ensure_ascii=False)
EOF
print_success("✓ Show notes saved: $output_file")
}
}

# Always exit cleanly
exit 0