#!/usr/bin/env python3
"""
YouTube Content Analyzer & Short-Form Generator
Analyzes existing YouTube videos and generates TikTok/YouTube Shorts content
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class VideoSegment:
    """Represents a segment of video content"""

    start_time: float
    end_time: float
    text: str
    engagement_score: float
    topic: str
    speaker: str
    duration: float


@dataclass
class YouTubeVideo:
    """Represents a YouTube video analysis"""

    video_id: str
    title: str
    description: str
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    publish_date: str
    transcript: Optional[str] = None
    segments: List[VideoSegment] = None

    def __post_init__(self):
        if self.segments is None:
            self.segments = []


class YouTubeContentAnalyzer:
    """Analyzes YouTube content and identifies high-value segments"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def analyze_channel(self, channel_id: str = "@JaredsNotFunny") -> Dict:
        """Analyze the YouTube channel for content patterns"""
        logger.info(f"Analyzing channel: {channel_id}")

        # For demo, use mock data from our search results
        videos = self._get_channel_videos(channel_id)

        analysis = {
            "channel_info": {
                "channel_id": channel_id,
                "subscriber_count": 85,  # From search results
                "video_count": len(videos),
                "total_views": sum(v.get("view_count", 0) for v in videos),
            },
            "content_analysis": self._analyze_content_patterns(videos),
            "optimization_suggestions": self._generate_optimization_suggestions(videos),
            "top_performers": self._identify_top_videos(videos),
        }

        return analysis

    def _get_channel_videos(self, channel_id: str) -> List[Dict]:
        """Get channel videos - using mock data from search results"""
        mock_videos = [
            {
                "video_id": "yCPDYXORg-A",
                "title": "JAREDSNOTFUNNY Feat Toron Rodgers #6",
                "description": "Jared Christianson sits down with Toron Rodgers as they discuss performing stand up comedy, production and life experiences.",
                "view_count": 131,
                "duration": "1:08:40",
                "publish_date": "2025-09-10",
            },
            {
                "video_id": "r3-HsQ6m6bs",
                "title": "JAREDSNOTFUNNY Feat Arthur Stump #9",
                "description": "JAREDSNOTFUNNY is proud to present one of Jared's most laid back and funniest comedians in the Roanoke valley Arthur Stump.",
                "view_count": 88,
                "duration": "58:40",
                "publish_date": "2025-09-15",
            },
            {
                "video_id": "QkPG-c5TjPc",
                "title": "JAREDSNOTFUNNY feat Christinia Tynes",
                "description": "Jared Christianson sits down with fellow local comedian Christinia Tynes and discuss all sorts of things while eating Bean Boozled.",
                "view_count": 42,
                "duration": "1:04:30",
                "publish_date": "2025-12-10",
            },
            {
                "video_id": "iyTR8jp1EQs",
                "title": "JAREDSNOTFUNNY Feat Jacob Davidson",
                "description": "Jared sits down with long time friend and scientist Jacob Davidson. Jacob talks about his road to becoming a scientist and what it's been like living in Germany.",
                "view_count": 31,
                "duration": "38:10",
                "publish_date": "2025-12-12",
            },
        ]
        return mock_videos

    def _analyze_content_patterns(self, videos: List[Dict]) -> Dict:
        """Analyze content patterns and themes"""
        titles = [v["title"] for v in videos]
        descriptions = [v["description"] for v in videos]

        # Extract common themes and patterns
        guest_names = self._extract_guest_names(titles)
        topics = self._extract_topics(descriptions)

        return {
            "content_frequency": {
                "total_videos": len(videos),
                "avg_views": sum(v["view_count"] for v in videos) / len(videos),
                "view_range": {
                    "min": min(v["view_count"] for v in videos),
                    "max": max(v["view_count"] for v in videos),
                },
            },
            "guest_analysis": guest_names,
            "topic_analysis": topics,
            "duration_analysis": self._analyze_durations(videos),
            "posting_frequency": self._calculate_posting_frequency(videos),
        }

    def _extract_guest_names(self, titles: List[str]) -> Dict:
        """Extract guest names from video titles"""
        guest_names = []
        for title in titles:
            # Pattern: JAREDSNOTFUNNY Feat [Guest Name]
            match = re.search(
                r"JAREDSNOTFUNNY.*?Feat\s+(.+?)(?:\s+#|$)", title, re.IGNORECASE
            )
            if match:
                guest_names.append(match.group(1).strip())

        return {
            "total_guests": len(guest_names),
            "guest_names": guest_names,
            "repeat_guests": [],  # Could implement detection logic
        }

    def _extract_topics(self, descriptions: List[str]) -> List[str]:
        """Extract common topics from descriptions"""
        all_text = " ".join(descriptions).lower()

        # Common podcast topics to look for
        topics_keywords = {
            "comedy": ["comedy", "funny", "stand-up", "stage", "perform"],
            "life experiences": ["life", "experiences", "story", "journey"],
            "career": ["career", "scientist", "artist", "recording"],
            "personal growth": ["overcome", "adversity", "strength", "growth"],
            "food": ["eating", "bean boozled", "pickle", "food"],
            "local": ["local", "roanoke", "valley"],
        }

        found_topics = []
        for topic, keywords in topics_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                found_topics.append(topic)

        return found_topics

    def _analyze_durations(self, videos: List[Dict]) -> Dict:
        """Analyze video duration patterns"""
        durations = []
        for video in videos:
            # Convert duration string to minutes
            parts = video["duration"].split(":")
            if len(parts) == 2:  # MM:SS
                minutes = int(parts[0]) + int(parts[1]) / 60
            elif len(parts) == 3:  # H:MM:SS
                minutes = int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
            else:
                continue
            durations.append(minutes)

        if not durations:
            return {"avg_duration": 0, "duration_range": {"min": 0, "max": 0}}

        return {
            "avg_duration": sum(durations) / len(durations),
            "duration_range": {"min": min(durations), "max": max(durations)},
            "unit": "minutes",
        }

    def _calculate_posting_frequency(self, videos: List[Dict]) -> Dict:
        """Calculate posting frequency based on dates"""
        # Simplified calculation based on mock data
        return {
            "frequency": "weekly",
            "consistency_score": 0.8,  # 0-1 scale
            "suggested_schedule": "Every Thursday",
        }

    def _identify_top_videos(self, videos: List[Dict]) -> List[Dict]:
        """Identify best performing videos"""
        sorted_videos = sorted(videos, key=lambda x: x["view_count"], reverse=True)
        return sorted_videos[:3]  # Top 3 videos

    def _generate_optimization_suggestions(self, videos: List[Dict]) -> List[str]:
        """Generate SEO and optimization suggestions"""
        suggestions = []

        avg_views = sum(v["view_count"] for v in videos) / len(videos)
        max_views = max(v["view_count"] for v in videos)

        if avg_views < 100:
            suggestions.append(
                "Focus on keyword optimization in titles and descriptions"
            )
            suggestions.append("Create more engaging thumbnails")
            suggestions.append("Add relevant hashtags to improve discoverability")

        if max_views - avg_views > 50:
            top_videos = self._identify_top_videos(videos)
            suggestions.append(
                f"Replicate format of top video: {top_videos[0]['title']}"
            )

        suggestions.append("Create short-form clips from high-engagement segments")
        suggestions.append("Optimize for YouTube SEO with relevant keywords")
        suggestions.append("Add timestamps for better user experience")

        return suggestions


class ShortFormContentGenerator:
    """Generates TikTok/YouTube Shorts content from full episodes"""

    def __init__(self):
        self.optimal_duration = 60  # seconds for TikTok/Shorts
        self.hook_keywords = [
            "hilarious",
            "shocking",
            "you won't believe",
            "must watch",
        ]

    def identify_viral_segments(self, video: YouTubeVideo) -> List[VideoSegment]:
        """Identify high-potential short-form segments"""
        segments = []

        # Mock analysis - in real implementation would use audio analysis
        mock_segments = [
            VideoSegment(
                start_time=120,  # 2 minutes
                end_time=180,  # 3 minutes
                text="Funniest moment about comedy career",
                engagement_score=8.5,
                topic="comedy",
                speaker="Jared",
                duration=60,
            ),
            VideoSegment(
                start_time=480,  # 8 minutes
                end_time=540,  # 9 minutes
                text="Hilarious reaction to pickle balls challenge",
                engagement_score=9.2,
                topic="food challenge",
                speaker="Both",
                duration=60,
            ),
        ]

        segments.extend(mock_segments)
        return sorted(segments, key=lambda x: x.engagement_score, reverse=True)

    def generate_tiktok_content(
        self, segment: VideoSegment, video: YouTubeVideo
    ) -> Dict:
        """Generate TikTok-optimized content from segment"""
        return {
            "platform": "TikTok",
            "content": {
                "hook": f"🔥 {segment.text[:50]}...",
                "body": f"From podcast with {self._extract_guest_name(video.title)}",
                "cta": "Follow @jaredsnotfunny for more!",
                "hashtags": self._generate_hashtags(segment.topic, video.title),
                "duration": segment.duration,
                "timestamp": segment.start_time,
            },
            "editing_instructions": {
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "text_overlays": [segment.text[:30]],
                "background_music": "trending comedy audio",
                "subtitles": True,
                "aspect_ratio": "9:16",
            },
            "metadata": {
                "source_video": video.video_id,
                "segment_score": segment.engagement_score,
                "topic": segment.topic,
            },
        }

    def generate_youtube_short(
        self, segment: VideoSegment, video: YouTubeVideo
    ) -> Dict:
        """Generate YouTube Shorts-optimized content"""
        return {
            "platform": "YouTube Shorts",
            "content": {
                "title": f"{segment.text[:40]}... #shorts #podcast",
                "description": f"Clip from JAREDSNOTFUNNY podcast episode with {self._extract_guest_name(video.title)}\\n\\nFull episode: https://youtu.be/{video.video_id}",
                "hashtags": self._generate_hashtags(
                    segment.topic, video.title, platform="youtube"
                ),
                "duration": segment.duration,
                "timestamp": segment.start_time,
            },
            "editing_instructions": {
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "text_overlays": ["JAREDSNOTFUNNY PODCAST", segment.text[:40]],
                "subtitles": True,
                "aspect_ratio": "9:16",
            },
            "metadata": {
                "source_video": video.video_id,
                "segment_score": segment.engagement_score,
                "topic": segment.topic,
            },
        }

    def _extract_guest_name(self, title: str) -> str:
        """Extract guest name from video title"""
        match = re.search(r"Feat\s+(.+?)(?:\s+#|$)", title, re.IGNORECASE)
        return match.group(1) if match else "Guest"

    def _generate_hashtags(
        self, topic: str, title: str, platform: str = "tiktok"
    ) -> List[str]:
        """Generate platform-specific hashtags"""
        base_hashtags = ["#jaredsnotfunny", "#podcast", "#comedy"]
        topic_hashtags = [f"#{topic.replace(' ', '')}"]

        if platform == "tiktok":
            base_hashtags.extend(["#fyp", "#foryou", "#viral"])
        elif platform == "youtube":
            base_hashtags.extend(["#shorts", "#podcastclips"])

        return base_hashtags + topic_hashtags


def analyze_and_generate_content():
    """Main function to analyze YouTube channel and generate short-form content"""
    print("🎬 YouTube Content Analysis & Short-Form Generation")
    print("=" * 60)

    # Initialize analyzers
    analyzer = YouTubeContentAnalyzer()
    generator = ShortFormContentGenerator()

    # Analyze channel
    print("📊 Analyzing YouTube Channel...")
    channel_analysis = analyzer.analyze_channel()

    print(f"✅ Channel Analysis Complete:")
    print(f"   📺 Total Videos: {channel_analysis['channel_info']['video_count']}")
    print(f"   👥 Subscribers: {channel_analysis['channel_info']['subscriber_count']}")
    print(f"   👀 Total Views: {channel_analysis['channel_info']['total_views']}")

    # Generate content suggestions
    print(f"\n🎯 Top Performing Videos:")
    for i, video in enumerate(channel_analysis["top_performers"], 1):
        print(f"   {i}. {video['title']} ({video['view_count']} views)")

    print(f"\n💡 Optimization Suggestions:")
    for suggestion in channel_analysis["optimization_suggestions"]:
        print(f"   • {suggestion}")

    # Generate short-form content from top video
    top_video_data = channel_analysis["top_performers"][0]
    top_video = YouTubeVideo(
        video_id=top_video_data["video_id"],
        title=top_video_data["title"],
        description=top_video_data["description"],
        duration=top_video_data["duration"],
        view_count=top_video_data["view_count"],
        like_count=0,
        comment_count=0,
        publish_date=top_video_data["publish_date"],
    )

    print(f"\n🚀 Generating Short-Form Content from: {top_video.title}")

    # Identify viral segments
    segments = generator.identify_viral_segments(top_video)

    # Generate content for each platform
    for i, segment in enumerate(segments, 1):
        print(
            f"\n📱 Segment {i}: {segment.text} (Score: {segment.engagement_score}/10)"
        )

        # TikTok content
        tiktok_content = generator.generate_tiktok_content(segment, top_video)
        print(f"   🎵 TikTok Hook: {tiktok_content['content']['hook']}")
        print(f"   🏷️  Hashtags: {' '.join(tiktok_content['content']['hashtags'][:5])}")

        # YouTube Short content
        youtube_content = generator.generate_youtube_short(segment, top_video)
        print(f"   📺 YouTube Title: {youtube_content['content']['title']}")
        print(f"   ⏱️  Duration: {youtube_content['content']['duration']}s")

    # Save results
    output_file = "content_analysis_results.json"
    results = {
        "channel_analysis": channel_analysis,
        "generated_content": [
            {
                "segment_index": i,
                "tiktok": generator.generate_tiktok_content(seg, top_video),
                "youtube_short": generator.generate_youtube_short(seg, top_video),
            }
            for i, seg in enumerate(segments)
        ],
    }

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {output_file}")
    print(f"🎉 Ready to generate {len(segments)} viral clips!")


if __name__ == "__main__":
    analyze_and_generate_content()
