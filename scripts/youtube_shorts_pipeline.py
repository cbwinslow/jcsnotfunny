"""YouTube Shorts Creation Pipeline

Complete pipeline for downloading YouTube videos, analyzing for funny moments,
and creating YouTube Shorts.

Usage:
  python scripts/youtube_shorts_pipeline.py --url "YOUTUBE_URL" --output-dir "OUTPUT_DIR"
"""

import argparse
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

# Setup logging
logger = logging.getLogger('youtube_shorts_pipeline')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(ch)


class YouTubeShortsPipeline:
    """Complete pipeline for YouTube shorts creation."""

    def __init__(self):
        """Initialize the pipeline."""
        # Import agents dynamically to avoid circular imports
        from agents.video_editing_agent import VideoEditingAgent
        from agents.transcription_agent import TranscriptionAgent
        from agents.funny_moment_agent import FunnyMomentAgent

        self.video_agent = VideoEditingAgent()
        self.transcription_agent = TranscriptionAgent()
        self.funny_moment_agent = FunnyMomentAgent()

    def run_pipeline(self, youtube_url: str, output_dir: str = "youtube_shorts",
                    min_clip_duration: float = 8.0, max_clip_duration: float = 60.0) -> Dict[str, Any]:
        """Run the complete YouTube shorts creation pipeline."""
        logger.info(f"Starting YouTube Shorts pipeline for: {youtube_url}")

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Step 1: Download YouTube video
        logger.info("Step 1/5: Downloading YouTube video...")
        video_info = self._download_youtube_video(youtube_url, output_dir)
        logger.info(f"Downloaded video: {video_info['video_path']}")

        # Step 2: Extract audio and transcribe
        logger.info("Step 2/5: Transcribing video...")
        transcript_info = self._transcribe_video(video_info['video_path'], output_dir)
        logger.info(f"Created transcript: {transcript_info['vtt_file']}")

        # Step 3: Analyze for funny moments
        logger.info("Step 3/5: Analyzing for funny moments...")
        funny_moments = self._analyze_funny_moments(transcript_info['vtt_file'], min_clip_duration, max_clip_duration)
        logger.info(f"Found {funny_moments['total_segments']} funny segments")

        # Step 4: Identify and create funny clips
        logger.info("Step 4/5: Creating funny clips...")
        clips_info = self._create_funny_clips(
            video_info['video_path'],
            transcript_info['vtt_file'],
            output_dir,
            min_clip_duration,
            max_clip_duration
        )
        logger.info(f"Created {clips_info['total_clips']} funny clips")

        # Step 5: Generate pipeline report
        logger.info("Step 5/5: Generating pipeline report...")
        report = self._generate_pipeline_report(
            youtube_url, video_info, transcript_info, funny_moments, clips_info
        )

        logger.info(f"Pipeline completed! Created {clips_info['total_clips']} clips in {output_dir}")

        return report

    def _download_youtube_video(self, url: str, output_dir: str) -> Dict[str, Any]:
        """Download YouTube video using video editing agent."""
        try:
            # Use video editing agent to download
            download_params = {
                "url": url,
                "output_path": os.path.join(output_dir, "original_video.mp4"),
                "quality": "best",
                "format": "mp4"
            }

            result = self.video_agent.execute_tool("download_video", download_params)

            return {
                "video_path": result["video_path"],
                "title": result["title"],
                "duration": result["duration"],
                "file_size": result["file_size"],
                "url": url
            }

        except Exception as e:
            logger.error(f"Failed to download YouTube video: {str(e)}")
            raise

    def _transcribe_video(self, video_path: str, output_dir: str) -> Dict[str, Any]:
        """Extract audio and transcribe video."""
        try:
            # First extract audio
            audio_output = os.path.join(output_dir, "audio.mp3")
            extract_params = {
                "input_video": video_path,
                "output_audio": audio_output,
                "format": "mp3",
                "bitrate": "192k"
            }

            audio_result = self.video_agent.execute_tool("extract_audio", extract_params)
            logger.info(f"Extracted audio: {audio_result['output_audio']}")

            # Then transcribe
            transcript_params = {
                "input_file": audio_result['output_audio'],
                "output_dir": output_dir,
                "backend": "whisper"
            }

            transcript_result = self.transcription_agent.execute_tool("transcribe_audio", transcript_params)

            return {
                "audio_file": audio_result['output_audio'],
                "vtt_file": transcript_result['vtt_file'],
                "json_file": transcript_result['json_file'],
                "transcript_text": transcript_result['transcript'],
                "duration": transcript_result['duration']
            }

        except Exception as e:
            logger.error(f"Failed to transcribe video: {str(e)}")
            raise

    def _analyze_funny_moments(self, transcript_path: str, min_duration: float, max_duration: float) -> Dict[str, Any]:
        """Analyze transcript for funny moments."""
        try:
            # Read transcript file
            with open(transcript_path, 'r') as f:
                transcript_content = f.read()

            # Analyze for funny moments
            analysis_params = {
                "transcript_text": transcript_content,
                "min_duration": min_duration,
                "max_duration": max_duration
            }

            result = self.funny_moment_agent.execute_tool("analyze_transcript", analysis_params)

            return {
                "funny_segments": result["funny_segments"],
                "total_segments": result["total_segments"],
                "analysis_method": result["analysis_method"]
            }

        except Exception as e:
            logger.error(f"Failed to analyze funny moments: {str(e)}")
            raise

    def _create_funny_clips(self, video_path: str, transcript_path: str, output_dir: str,
                           min_duration: float, max_duration: float) -> Dict[str, Any]:
        """Create funny clips from video."""
        try:
            clips_output_dir = os.path.join(output_dir, "funny_clips")
            Path(clips_output_dir).mkdir(parents=True, exist_ok=True)

            # Identify funny clips
            clip_params = {
                "video_path": video_path,
                "transcript_path": transcript_path,
                "output_dir": clips_output_dir,
                "min_clip_duration": min_duration,
                "max_clip_duration": max_duration
            }

            result = self.funny_moment_agent.execute_tool("identify_funny_clips", clip_params)

            # Actually create the video clips
            self._generate_video_clips(result["funny_clips"])

            return {
                "funny_clips": result["funny_clips"],
                "total_clips": result["total_clips"],
                "output_dir": result["output_dir"],
                "clips_info_file": result["clips_info_file"]
            }

        except Exception as e:
            logger.error(f"Failed to create funny clips: {str(e)}")
            raise

    def _generate_video_clips(self, clips: List[Dict[str, Any]]) -> None:
        """Generate actual video clips using ffmpeg."""
        for clip in clips:
            try:
                # Use video editing agent to trim video
                trim_params = {
                    "input_video": clip["video_path"],
                    "output_video": clip["output_path"],
                    "start_time": clip["start_time"],
                    "end_time": clip["end_time"]
                }

                result = self.video_agent.execute_tool("trim_video", trim_params)
                logger.info(f"Created clip: {result['output_video']} ({result['duration']}s)")

            except Exception as e:
                logger.warning(f"Failed to create clip {clip['clip_id']}: {str(e)}")

    def _generate_pipeline_report(self, youtube_url: str, video_info: Dict[str, Any],
                                 transcript_info: Dict[str, Any], funny_moments: Dict[str, Any],
                                 clips_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive pipeline report."""
        report = {
            "youtube_url": youtube_url,
            "video_info": {
                "title": video_info.get("title", "Unknown"),
                "duration": video_info.get("duration", 0),
                "file_size": video_info.get("file_size", 0),
                "path": video_info.get("video_path", "")
            },
            "transcript_info": {
                "vtt_file": transcript_info.get("vtt_file", ""),
                "json_file": transcript_info.get("json_file", ""),
                "duration": transcript_info.get("duration", 0),
                "has_transcript": bool(transcript_info.get("transcript_text"))
            },
            "funny_moment_analysis": {
                "total_segments": funny_moments.get("total_segments", 0),
                "analysis_method": funny_moments.get("analysis_method", "unknown"),
                "segments": [
                    {
                        "start_time": seg["start_time"],
                        "end_time": seg["end_time"],
                        "funny_score": seg["funny_score"],
                        "text": seg["text"][:100] + "..." if len(seg["text"]) > 100 else seg["text"]
                    }
                    for seg in funny_moments.get("funny_segments", [])
                ]
            },
            "clips_created": {
                "total_clips": clips_info.get("total_clips", 0),
                "output_dir": clips_info.get("output_dir", ""),
                "clips_info_file": clips_info.get("clips_info_file", ""),
                "clips": [
                    {
                        "clip_id": clip["clip_id"],
                        "start_time": clip["start_time"],
                        "end_time": clip["end_time"],
                        "duration": clip["duration"],
                        "funny_score": clip["funny_score"],
                        "output_path": clip["output_path"]
                    }
                    for clip in clips_info.get("funny_clips", [])
                ]
            },
            "summary": {
                "status": "completed",
                "total_funny_segments": funny_moments.get("total_segments", 0),
                "total_clips_created": clips_info.get("total_clips", 0),
                "success_rate": clips_info.get("total_clips", 0) / max(1, funny_moments.get("total_segments", 1))
            }
        }

        # Save report to file
        report_file = os.path.join(clips_info.get("output_dir", "youtube_shorts"), "pipeline_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        report["report_file"] = report_file

        return report


def main():
    """Main entry point for YouTube Shorts pipeline."""
    parser = argparse.ArgumentParser(description="YouTube Shorts Creation Pipeline")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--output-dir", default="youtube_shorts", help="Output directory")
    parser.add_argument("--min-duration", type=float, default=8.0, help="Minimum clip duration in seconds")
    parser.add_argument("--max-duration", type=float, default=60.0, help="Maximum clip duration in seconds")

    args = parser.parse_args()

    try:
        # Initialize and run pipeline
        pipeline = YouTubeShortsPipeline()
        result = pipeline.run_pipeline(
            youtube_url=args.url,
            output_dir=args.output_dir,
            min_clip_duration=args.min_duration,
            max_clip_duration=args.max_duration
        )

        logger.info(f"\n=== PIPELINE COMPLETED ===")
        logger.info(f"YouTube URL: {args.url}")
        logger.info(f"Funny segments found: {result['funny_moment_analysis']['total_segments']}")
        logger.info(f"Clips created: {result['clips_created']['total_clips']}")
        logger.info(f"Output directory: {result['clips_created']['output_dir']}")
        logger.info(f"Report saved to: {result['report_file']}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
