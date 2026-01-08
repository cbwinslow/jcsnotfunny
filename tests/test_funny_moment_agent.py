"""Comprehensive tests for Funny Moment Agent.

Tests all toolsets, validation, error handling, and output quality.
"""

import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from agents.funny_moment_agent import (
    FunnyMomentAgent,
    TranscriptAnalysisTool,
    LaughterDetectionTool,
    FunnyClipIdentificationTool
)


class TestFunnyMomentAgent(unittest.TestCase):
    """Test suite for Funny Moment Agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = FunnyMomentAgent()
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.test_data_dir.mkdir(exist_ok=True)

        # Create test transcript
        self.test_transcript = self.test_data_dir / "test_transcript.txt"
        with open(self.test_transcript, 'w') as f:
            f.write("""This is a funny joke that will make you laugh out loud.
The audience is laughing hysterically at this point.
LOL that was hilarious!
This is some serious content without jokes.
Ha ha ha, that's the funniest thing I've heard all day!
Another funny moment with jokes and comedy.
""")

    def tearDown(self):
        """Clean up test files."""
        # Remove test data directory
        for file in self.test_data_dir.glob("*"):
            file.unlink()
        self.test_data_dir.rmdir()

    def test_agent_initialization(self):
        """Test that agent initializes with correct tools."""
        tools = self.agent.get_available_tools()
        expected_tools = ["analyze_transcript", "detect_laughter", "identify_funny_clips"]

        self.assertEqual(len(tools), 3)
        for tool_name in expected_tools:
            self.assertIn(tool_name, tools)

    def test_transcript_analysis_tool(self):
        """Test transcript analysis tool functionality."""
        tool = TranscriptAnalysisTool()

        # Test with funny content
        funny_text = "This is a hilarious joke! LOL that was so funny, I can't stop laughing."
        result = tool.execute({"transcript_text": funny_text})

        # ToolResult has a data attribute
        self.assertTrue(result.success)
        self.assertIn("funny_segments", result.data)
        self.assertGreater(result.data["total_segments"], 0)
        self.assertEqual(result.data["analysis_method"], "keyword_and_pattern_based")

        # Verify funny segments have proper structure
        for segment in result.data["funny_segments"]:
            self.assertIn("start_time", segment)
            self.assertIn("end_time", segment)
            self.assertIn("text", segment)
            self.assertIn("funny_score", segment)
            self.assertGreater(segment["funny_score"], 0)

    def test_transcript_analysis_with_non_funny_content(self):
        """Test transcript analysis with non-funny content."""
        tool = TranscriptAnalysisTool()

        # Test with serious content
        serious_text = "This is a serious discussion about important topics. No jokes here."
        result = tool.execute({"transcript_text": serious_text})

        self.assertTrue(result.success)
        self.assertIn("funny_segments", result.data)
        self.assertEqual(result.data["total_segments"], 0)

    def test_transcript_analysis_duration_constraints(self):
        """Test duration constraints in transcript analysis."""
        tool = TranscriptAnalysisTool()

        funny_text = "Funny joke here. " * 20  # Long funny content

        # Test with minimum duration
        result_min = tool.execute({
            "transcript_text": funny_text,
            "min_duration": 10.0,
            "max_duration": 30.0
        })

        self.assertTrue(result_min.success)
        # Verify all segments meet minimum duration
        for segment in result_min.data["funny_segments"]:
            duration = segment["end_time"] - segment["start_time"]
            self.assertGreaterEqual(duration, 10.0)
            self.assertLessEqual(duration, 30.0)

    def test_laughter_detection_tool(self):
        """Test laughter detection tool."""
        tool = LaughterDetectionTool()

        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
            # Write some dummy data
            temp_audio.write(b"RIFF" + b"\x00" * 100)

        try:
            # Test laughter detection
            result = tool.execute({"audio_file": temp_audio_path})

            self.assertTrue(result.success)
            self.assertIn("laughter_segments", result.data)
            self.assertIn("total_laughter", result.data)
            self.assertEqual(result.data["detection_method"], "basic_audio_analysis")

            # Test with output file
            output_path = str(self.test_data_dir / "laughter_results.json")
            result_with_output = tool.execute({
                "audio_file": temp_audio_path,
                "output_file": output_path
            })

            # Verify output file was created
            self.assertTrue(Path(output_path).exists())

            # Verify output file content
            with open(output_path, 'r') as f:
                output_data = json.load(f)
                self.assertIn("laughter_segments", output_data)

        finally:
            # Clean up temp file
            os.unlink(temp_audio_path)

    def test_laughter_detection_file_not_found(self):
        """Test laughter detection with non-existent file."""
        tool = LaughterDetectionTool()

        with self.assertRaises(FileNotFoundError):
            tool.execute({"audio_file": "/non/existent/file.mp3"})

    def test_funny_clip_identification_tool(self):
        """Test funny clip identification tool."""
        tool = FunnyClipIdentificationTool()

        # Create test files
        test_video = self.test_data_dir / "test_video.mp4"
        test_transcript = self.test_data_dir / "test_transcript.vtt"

        # Create dummy video file
        with open(test_video, 'wb') as f:
            f.write(b"FAKEVIDEO" + b"\x00" * 1000)

        # Create VTT transcript
        vtt_content = """WEBVTT

00:00:00.000 --> 00:00:10.000
This is a funny joke that will make you laugh.

00:00:10.000 --> 00:00:20.000
Serious content without any humor.

00:00:20.000 --> 00:00:30.000
LOL that was hilarious! Best joke ever.

00:00:30.000 --> 00:00:40.000
More funny content with jokes and comedy.
"""

        with open(test_transcript, 'w') as f:
            f.write(vtt_content)

        try:
            # Test clip identification
            result = tool.execute({
                "video_path": str(test_video),
                "transcript_path": str(test_transcript),
                "output_dir": str(self.test_data_dir),
                "min_clip_duration": 5.0,
                "max_clip_duration": 15.0
            })

            self.assertTrue(result.success)
            self.assertIn("funny_clips", result.data)
            self.assertGreater(result.data["total_clips"], 0)
            self.assertTrue(Path(result.data["output_dir"]).exists())
            self.assertTrue(Path(result.data["clips_info_file"]).exists())

            # Verify clips have proper structure
            for clip in result.data["funny_clips"]:
                self.assertIn("clip_id", clip)
                self.assertIn("start_time", clip)
                self.assertIn("end_time", clip)
                self.assertIn("duration", clip)
                self.assertIn("funny_score", clip)
                self.assertIn("output_path", clip)

                # Verify duration constraints
                self.assertGreaterEqual(clip["duration"], 5.0)
                self.assertLessEqual(clip["duration"], 15.0)

        finally:
            # Clean up test files
            test_video.unlink()
            test_transcript.unlink()

    def test_funny_clip_identification_file_errors(self):
        """Test funny clip identification with file errors."""
        tool = FunnyClipIdentificationTool()

        # Test with non-existent video file
        with self.assertRaises(FileNotFoundError):
            tool.execute({
                "video_path": "/non/existent/video.mp4",
                "transcript_path": str(self.test_transcript)
            })

        # Test with non-existent transcript file
        with self.assertRaises(FileNotFoundError):
            tool.execute({
                "video_path": str(self.test_transcript),  # Using transcript as video
                "transcript_path": "/non/existent/transcript.vtt"
            })

    def test_funny_score_calculation(self):
        """Test funny score calculation logic."""
        tool = TranscriptAnalysisTool()

        # Test text with multiple funny elements
        text = "LOL that was hilarious! Ha ha ha, what a funny joke! LMAO!"
        result = tool.execute({"transcript_text": text})

        # Should find at least one funny segment
        self.assertTrue(result.success)
        self.assertGreater(len(result.data["funny_segments"]), 0)

        # Check that funny score is reasonable
        for segment in result.data["funny_segments"]:
            if "LOL" in segment["text"] or "hilarious" in segment["text"]:
                self.assertGreater(segment["funny_score"], 1.0)

    def test_vtt_parsing(self):
        """Test VTT file parsing functionality."""
        tool = FunnyClipIdentificationTool()

        # Create test VTT file
        vtt_content = """WEBVTT

00:00:01.500 --> 00:00:05.200
First segment with funny content.

00:00:06.000 --> 00:00:12.800
Second segment that's also funny.

00:00:13.200 --> 00:00:18.900
Third funny segment here.
"""

        vtt_file = self.test_data_dir / "test_parsing.vtt"
        with open(vtt_file, 'w') as f:
            f.write(vtt_content)

        try:
            # Parse the VTT file
            segments = tool._parse_vtt(str(vtt_file))

            self.assertEqual(len(segments), 3)

            # Verify first segment
            self.assertAlmostEqual(segments[0]["start"], 1.5, places=1)
            self.assertAlmostEqual(segments[0]["end"], 5.2, places=1)
            self.assertEqual(segments[0]["text"], "First segment with funny content.")

        finally:
            vtt_file.unlink()

    def test_json_transcript_parsing(self):
        """Test JSON transcript parsing functionality."""
        tool = FunnyClipIdentificationTool()

        # Create test JSON file
        json_content = {
            "segments": [
                {"start": 0.0, "end": 5.0, "text": "Funny joke here"},
                {"start": 5.0, "end": 10.0, "text": "Another funny moment"},
                {"start": 10.0, "end": 15.0, "text": "Serious content"}
            ]
        }

        json_file = self.test_data_dir / "test_parsing.json"
        with open(json_file, 'w') as f:
            json.dump(json_content, f)

        try:
            # Parse the JSON file
            segments = tool._parse_transcript(str(json_file))

            self.assertEqual(len(segments), 3)
            self.assertEqual(segments[0]["text"], "Funny joke here")

        finally:
            json_file.unlink()

    def test_time_parsing(self):
        """Test time parsing functionality."""
        tool = FunnyClipIdentificationTool()

        # Test various time formats
        test_cases = [
            ("00:00:01.500", 1.5),
            ("00:01:30.250", 90.25),
            ("01:05:20.750", 3920.75),
            ("00:00:05,500", 5.5),  # Comma separator
            ("00:01:30", 90.0),     # No milliseconds
        ]

        for time_str, expected_seconds in test_cases:
            result = tool._parse_time(time_str)
            self.assertAlmostEqual(result, expected_seconds, places=2)

    def test_agent_integration(self):
        """Test agent integration with all tools."""
        # Test that agent can execute all tools
        tools = self.agent.get_available_tools()

        # Test analyze_transcript tool
        transcript_result = self.agent.execute_tool("analyze_transcript", {
            "transcript_text": "This is a funny joke! LOL!"
        })
        self.assertTrue(transcript_result.success)
        self.assertIn("funny_segments", transcript_result.data)

        # Test detect_laughter tool (with mock file)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
            temp_audio.write(b"RIFF" + b"\x00" * 100)

        try:
            laughter_result = self.agent.execute_tool("detect_laughter", {
                "audio_file": temp_audio_path
            })
            self.assertTrue(laughter_result.success)
            self.assertIn("laughter_segments", laughter_result.data)
        finally:
            os.unlink(temp_audio_path)


class TestFunnyMomentAgentPerformance(unittest.TestCase):
    """Performance and edge case tests for Funny Moment Agent."""

    def setUp(self):
        """Set up performance test fixtures."""
        self.agent = FunnyMomentAgent()

    def test_large_transcript_performance(self):
        """Test performance with large transcripts."""
        tool = TranscriptAnalysisTool()

        # Create large transcript
        large_text = "Funny joke. " * 1000 + "Serious content. " * 1000

        # This should complete in reasonable time
        result = tool.execute({"transcript_text": large_text})

        self.assertIsNotNone(result)
        self.assertIn("funny_segments", result)

    def test_empty_transcript(self):
        """Test with empty transcript."""
        tool = TranscriptAnalysisTool()

        result = tool.execute({"transcript_text": ""})

        self.assertTrue(result.success)
        self.assertEqual(result.data["total_segments"], 0)
        self.assertEqual(len(result.data["funny_segments"]), 0)

    def test_special_characters_in_transcript(self):
        """Test transcript with special characters."""
        tool = TranscriptAnalysisTool()

        special_text = "Funny joke! 😂🤣 LOL! #comedy #funny"
        result = tool.execute({"transcript_text": special_text})

        self.assertTrue(result.success)
        self.assertGreater(result.data["total_segments"], 0)

    def test_mixed_language_content(self):
        """Test with mixed language content."""
        tool = TranscriptAnalysisTool()

        mixed_text = "This is funny! Esto es gracioso! C'est drôle! Das ist lustig!"
        result = tool.execute({"transcript_text": mixed_text})

        # Should still detect English funny keywords
        self.assertTrue(result.success)
        self.assertGreater(result.data["total_segments"], 0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)



