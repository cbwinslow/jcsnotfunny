#!/usr/bin/env python3
"""
Automated Video Processing Pipeline
Converts full podcast episodes into short-form content for TikTok/YouTube Shorts
"""

import os
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class VideoClip:
    """Represents a video clip with metadata"""

    start_time: float
    end_time: float
    duration: float
    text: str
    engagement_score: float
    topic: str
    guest_name: str


class VideoProcessor:
    """Processes video files to create short-form content"""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="jaredsnotfunny_")
        self.supported_formats = [".mp4", ".mov", ".avi", ".mkv"]

    def extract_clip(self, input_video: str, clip: VideoClip, output_path: str) -> bool:
        """Extract a clip from video using ffmpeg"""
        try:
            # Extract video clip
            cmd = [
                "ffmpeg",
                "-i",
                input_video,
                "-ss",
                str(clip.start_time),
                "-t",
                str(clip.duration),
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-preset",
                "fast",
                "-y",
                output_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False

            logger.info(f"Extracted clip: {clip.start_time}s - {clip.end_time}s")
            return True

        except Exception as e:
            logger.error(f"Clip extraction failed: {e}")
            return False

    def resize_for_tiktok(self, input_video: str, output_video: str) -> bool:
        """Resize video to 9:16 aspect ratio for TikTok/Shorts"""
        try:
            cmd = [
                "ffmpeg",
                "-i",
                input_video,
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-preset",
                "fast",
                "-y",
                output_video,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Resize error: {result.stderr}")
                return False

            logger.info(f"Resized video for TikTok: {output_video}")
            return True

        except Exception as e:
            logger.error(f"Video resize failed: {e}")
            return False

    def add_subtitles(
        self, input_video: str, subtitle_text: str, output_video: str
    ) -> bool:
        """Add hard subtitles to video"""
        try:
            # Create temporary subtitle file
            subtitle_file = os.path.join(self.temp_dir, "subtitle.srt")

            # Simple SRT format
            srt_content = f"""1
00:00:00,000 --> 00:00:05,000
{subtitle_text}

2
00:00:05,000 --> 00:00:10,000  
{subtitle_text}

3
00:00:10,000 --> 00:01:00,000
{subtitle_text}
"""

            with open(subtitle_file, "w") as f:
                f.write(srt_content)

            # Burn subtitles into video
            cmd = [
                "ffmpeg",
                "-i",
                input_video,
                "-i",
                subtitle_file,
                "-vf",
                "subtitles=subtitle.srt",
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-preset",
                "fast",
                "-y",
                output_video,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Subtitle error: {result.stderr}")
                return False

            logger.info(f"Added subtitles: {output_video}")
            return True

        except Exception as e:
            logger.error(f"Subtitle addition failed: {e}")
            return False


class AutomatedContentPipeline:
    """Automated pipeline for generating short-form content"""

    def __init__(self):
        self.processor = VideoProcessor()
        self.output_dir = "generated_clips"

        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)

    def identify_viral_segments(
        self, transcript: str, video_duration: float
    ) -> List[VideoClip]:
        """Identify potentially viral segments from transcript"""
        # Viral indicators (simplified for demo)
        viral_keywords = [
            "hilarious",
            "funny story",
            "crazy",
            "insane",
            "can't believe",
            "you won't believe",
            "shocking",
            "amazing",
            "incredible",
            "pickles",
            "bean boozled",
            "comedy club",
            "stage fright",
        ]

        segments = []

        # Mock segments based on transcript analysis
        mock_segments = [
            VideoClip(
                start_time=120,  # 2:00
                end_time=180,  # 3:00
                duration=60,
                text="Hilarious story about first comedy show",
                engagement_score=8.5,
                topic="comedy stories",
                guest_name="Toron Rodgers",
            ),
            VideoClip(
                start_time=480,  # 8:00
                end_time=540,  # 9:00
                duration=60,
                text="Bean Boozled challenge gone wrong",
                engagement_score=9.2,
                topic="food challenge",
                guest_name="Christinia Tynes",
            ),
            VideoClip(
                start_time=720,  # 12:00
                end_time=780,  # 13:00
                duration=60,
                text="Living in Germany as a scientist",
                engagement_score=7.8,
                topic="life stories",
                guest_name="Jacob Davidson",
            ),
        ]

        # Filter for engagement score
        viral_segments = [seg for seg in mock_segments if seg.engagement_score >= 7.5]
        return sorted(viral_segments, key=lambda x: x.engagement_score, reverse=True)

    def generate_tiktok_content(self, clip: VideoClip, source_video: str) -> Dict:
        """Generate TikTok-optimized content"""
        clip_filename = f"tiktok_{clip.start_time}_{clip.end_time}.mp4"
        temp_clip = os.path.join(self.processor.temp_dir, f"temp_{clip_filename}")
        final_clip = os.path.join(self.output_dir, clip_filename)

        try:
            # Extract clip
            if not self.processor.extract_clip(source_video, clip, temp_clip):
                return {"success": False, "error": "Failed to extract clip"}

            # Resize for TikTok
            if not self.processor.resize_for_tiktok(temp_clip, temp_clip):
                return {"success": False, "error": "Failed to resize video"}

            # Add subtitles
            subtitle_text = (
                f"JAREDSNOTFUNNY feat {clip.guest_name}\\n{clip.text[:40]}..."
            )
            if not self.processor.add_subtitles(temp_clip, subtitle_text, final_clip):
                return {"success": False, "error": "Failed to add subtitles"}

            # Generate content metadata
            return {
                "success": True,
                "file_path": final_clip,
                "platform": "TikTok",
                "metadata": {
                    "title": f"🔥 {clip.text[:50]}...",
                    "description": f"Hilarious clip from JAREDSNOTFUNNY podcast with {clip.guest_name}\\n\\nFull episode on YouTube!\\n#jaredsnotfunny #podcast #comedy #fyp",
                    "duration": clip.duration,
                    "engagement_score": clip.engagement_score,
                    "topic": clip.topic,
                    "hashtags": [
                        "#jaredsnotfunny",
                        "#podcast",
                        "#comedy",
                        "#fyp",
                        "#funny",
                    ],
                    "posting_schedule": "Optimal: 7-9 PM, Tue/Wed/Thu",
                },
                "posting_instructions": {
                    "call_to_action": "Follow @jaredsnotfunny for full episodes!",
                    "engagement_prompt": "What's the funniest podcast moment you've heard?",
                    "tag_suggestions": [
                        "@jaredsnotfunny",
                        f"#{clip.guest_name.replace(' ', '')}",
                    ],
                },
            }

        except Exception as e:
            logger.error(f"TikTok content generation failed: {e}")
            return {"success": False, "error": str(e)}

    def generate_youtube_short(self, clip: VideoClip, source_video: str) -> Dict:
        """Generate YouTube Shorts content"""
        clip_filename = f"shorts_{clip.start_time}_{clip.end_time}.mp4"
        temp_clip = os.path.join(self.processor.temp_dir, f"temp_{clip_filename}")
        final_clip = os.path.join(self.output_dir, clip_filename)

        try:
            # Extract clip
            if not self.processor.extract_clip(source_video, clip, temp_clip):
                return {"success": False, "error": "Failed to extract clip"}

            # Resize for YouTube Shorts
            if not self.processor.resize_for_tiktok(temp_clip, temp_clip):
                return {"success": False, "error": "Failed to resize video"}

            # Add subtitles
            subtitle_text = f"JAREDSNOTFUNNY PODCAST\\n{clip.text[:40]}..."
            if not self.processor.add_subtitles(temp_clip, subtitle_text, final_clip):
                return {"success": False, "error": "Failed to add subtitles"}

            # Generate content metadata
            return {
                "success": True,
                "file_path": final_clip,
                "platform": "YouTube Shorts",
                "metadata": {
                    "title": f"{clip.text[:45]}... #shorts #podcast #jaredsnotfunny",
                    "description": f"Clip from JAREDSNOTFUNNY podcast featuring {clip.guest_name}\\n\\n🎥 Full episode: [link to full video]\\n\\n#jaredsnotfunny #podcast #comedy #shorts",
                    "tags": [
                        "jaredsnotfunny",
                        "podcast clips",
                        "comedy",
                        "funny moments",
                        clip.guest_name,
                    ],
                    "duration": clip.duration,
                    "engagement_score": clip.engagement_score,
                    "category": "Entertainment",
                },
                "seo_optimization": {
                    "thumbnail_suggestion": "Jared + guest laughing moment",
                    "end_screen": "Subscribe & watch full episode",
                    "cards": "Link to full podcast episode",
                    "upload_schedule": "Daily optimal: 6-8 PM",
                },
            }

        except Exception as e:
            logger.error(f"YouTube Shorts generation failed: {e}")
            return {"success": False, "error": str(e)}

    def process_full_episode(
        self, video_path: str, transcript: str, guest_name: str
    ) -> Dict:
        """Process a full episode and generate multiple clips"""
        logger.info(f"Processing episode: {video_path}")

        # Get video duration
        try:
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
        except:
            duration = 3600  # Default to 1 hour

        # Identify viral segments
        segments = self.identify_viral_segments(transcript, duration)

        results = {
            "success": True,
            "source_video": video_path,
            "guest_name": guest_name,
            "total_segments_found": len(segments),
            "generated_clips": [],
        }

        # Process each segment
        for i, segment in enumerate(segments, 1):
            logger.info(f"Generating content for segment {i}/{len(segments)}")

            # Generate TikTok content
            tiktok_result = self.generate_tiktok_content(segment, video_path)

            # Generate YouTube Short content
            youtube_result = self.generate_youtube_short(segment, video_path)

            clip_data = {
                "segment_id": i,
                "segment": segment,
                "tiktok": tiktok_result,
                "youtube_short": youtube_result,
                "priority": "High" if segment.engagement_score >= 8.5 else "Medium",
            }

            results["generated_clips"].append(clip_data)

        # Cleanup temp files
        self._cleanup()

        return results

    def _cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil

            shutil.rmtree(self.processor.temp_dir, ignore_errors=True)
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")


def create_sample_processing_pipeline():
    """Create a sample processing pipeline for demonstration"""
    print("🚀 Automated Video Processing Pipeline")
    print("=" * 50)

    pipeline = AutomatedContentPipeline()

    # Simulate processing a new episode
    mock_video_path = "/path/to/new_episode.mp4"  # Would be actual video file
    mock_transcript = """
    Jared: Welcome to JAREDSNOTFUNNY! Today I'm here with Toron Rodgers.
    Toron: Thanks for having me! I've got some hilarious stories about my first comedy show.
    Jared: Oh really? Tell us about that!
    Toron: So I get on stage, and my hands are shaking so bad...
    """
    mock_guest = "Toron Rodgers"

    print("📹 Processing mock episode...")
    print(f"   Guest: {mock_guest}")
    print(f"   Transcript length: {len(mock_transcript)} characters")

    # Process the episode
    results = pipeline.process_full_episode(
        mock_video_path, mock_transcript, mock_guest
    )

    if results["success"]:
        print(f"\\n✅ Processing Complete!")
        print(f"   📊 Segments Found: {results['total_segments_found']}")
        print(f"   🎬 Clips Generated: {len(results['generated_clips'])}")

        for clip in results["generated_clips"]:
            priority = clip["priority"]
            tiktok_status = "✅" if clip["tiktok"]["success"] else "❌"
            youtube_status = "✅" if clip["youtube_short"]["success"] else "❌"

            print(f"\\n   🎯 Segment {clip['segment_id']} ({priority} Priority):")
            print(f"      📱 TikTok: {tiktok_status}")
            print(f"      📺 YouTube: {youtube_status}")
            print(f"      💯 Score: {clip['segment'].engagement_score}/10")
            print(f"      🎪 Topic: {clip['segment'].topic}")

        print(f"\\n📁 Output Directory: {pipeline.output_dir}")
        print("🚀 Ready to post to social media!")

    return results


if __name__ == "__main__":
    create_sample_processing_pipeline()
