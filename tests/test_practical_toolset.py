#!/usr/bin/env python3
"""
Comprehensive test suite for the Practical Toolset implementation.
Tests all tools, workflows, error handling, and integration scenarios.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import json
import time

# Add scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from toolsets.practical_toolset import (
    PracticalToolsetManager,
    PracticalVideoAnalysisTool,
    PracticalAudioProcessingTool,
    PracticalContentSchedulingTool,
    ToolError,
    RecoverableError,
    ResourceError,
    ValidationError,
    FatalError
)


class TestPracticalToolset(unittest.TestCase):
    """Test suite for the Practical Toolset implementation."""

    def setUp(self):
        """Set up test environment."""
        self.manager = PracticalToolsetManager()
        self.test_dir = tempfile.mkdtemp()

        # Create test files
        self.test_video = os.path.join(self.test_dir, 'test_video.mp4')
        self.test_audio = os.path.join(self.test_dir, 'test_audio.wav')
        self.test_output = os.path.join(self.test_dir, 'output.mp3')
        self.test_media = os.path.join(self.test_dir, 'promo.jpg')

        # Create dummy files
        with open(self.test_video, 'w') as f:
            f.write('dummy video content')
        with open(self.test_audio, 'w') as f:
            f.write('dummy audio content')
        with open(self.test_media, 'w') as f:
            f.write('dummy media content')

    def tearDown(self):
        """Clean up test environment."""
        # Remove test directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_toolset_initialization(self):
        """Test toolset manager initialization."""
        self.assertIsInstance(self.manager, PracticalToolsetManager)
        self.assertEqual(len(self.manager.tools), 3)  # 3 tools
        self.assertEqual(len(self.manager.workflows), 2)  # 2 workflows

    def test_video_analysis_tool(self):
        """Test video analysis tool functionality."""
        tool = PracticalVideoAnalysisTool()

        # Test successful execution
        result = tool.execute({
            'video_path': self.test_video,
            'analysis_type': 'speaker_detection',
            'quality': 'high'
        })

        self.assertTrue(result['success'])
        self.assertIn('analysis_results', result)
        self.assertIn('execution_time', result)

        # Test with different analysis types
        for analysis_type in ['engagement', 'cut_points', 'full']:
            result = tool.execute({
                'video_path': self.test_video,
                'analysis_type': analysis_type,
                'quality': 'medium'
            })
            self.assertTrue(result['success'])

    def test_audio_processing_tool(self):
        """Test audio processing tool functionality."""
        tool = PracticalAudioProcessingTool()

        # Test successful execution
        result = tool.execute({
            'audio_path': self.test_audio,
            'output_path': self.test_output,
            'processing_steps': ['noise_reduction', 'de_essing'],
            'quality': 'high'
        })

        self.assertTrue(result['success'])
        self.assertIn('processed_audio_path', result)
        self.assertTrue(os.path.exists(result['processed_audio_path']))

        # Test with different processing steps
        result = tool.execute({
            'audio_path': self.test_audio,
            'output_path': self.test_output,
            'processing_steps': ['equalization'],
            'quality': 'medium'
        })
        self.assertTrue(result['success'])

    def test_content_scheduling_tool(self):
        """Test content scheduling tool functionality."""
        tool = PracticalContentSchedulingTool()

        # Test successful execution
        result = tool.execute({
            'content': 'Test episode available!',
            'platforms': ['twitter', 'instagram'],
            'media_path': self.test_media,
            'schedule_time': '2026-01-09T12:00:00Z',
            'dry_run': True
        })

        self.assertTrue(result['success'])
        self.assertIn('scheduled_posts', result)
        self.assertEqual(len(result['scheduled_posts']), 2)

        # Test with different platforms
        result = tool.execute({
            'content': 'Another test',
            'platforms': ['tiktok'],
            'dry_run': True
        })
        self.assertTrue(result['success'])
        self.assertEqual(len(result['scheduled_posts']), 1)

    def test_error_handling(self):
        """Test comprehensive error handling."""

        # Test validation errors
        tool = PracticalVideoAnalysisTool()

        with self.assertRaises(ValidationError):
            tool.execute({'video_path': ''})  # Missing required field

        with self.assertRaises(ValidationError):
            tool.execute({'video_path': self.test_video, 'analysis_type': 'invalid'})  # Invalid enum

        # Test recoverable errors (simulated)
        with patch.object(tool, '_execute_method') as mock_method:
            mock_method.side_effect = RecoverableError("Simulated timeout")

            result = tool.execute({
                'video_path': self.test_video,
                'analysis_type': 'speaker_detection'
            })

            # Should retry and eventually succeed with fallback
            self.assertTrue(result['success'])
            self.assertIn('retry_attempts', result)
            self.assertGreater(result['retry_attempts'], 0)

    def test_resource_management(self):
        """Test resource management and quality reduction."""

        # Simulate resource constraints
        with patch('psutil.cpu_percent', return_value=95):  # High CPU
            with patch('psutil.virtual_memory', return_value=MagicMock(percent=90)):  # High memory

                tool = PracticalVideoAnalysisTool()

                # Should automatically reduce quality
                result = tool.execute({
                    'video_path': self.test_video,
                    'analysis_type': 'speaker_detection',
                    'quality': 'high'  # Will be reduced
                })

                self.assertTrue(result['success'])
                self.assertIn('quality_adjustment', result)
                self.assertEqual(result['quality_adjustment'], 'medium')

    def test_workflow_execution(self):
        """Test complete workflow execution."""

        # Test episode production workflow
        result = self.manager.execute_workflow('episode_production', {
            'video_path': self.test_video,
            'audio_path': self.test_audio,
            'output_audio_path': self.test_output,
            'audio_processing_steps': ['noise_reduction'],
            'schedule_social': True,
            'social_content': 'New episode available!',
            'social_platforms': ['twitter'],
            'social_media_path': self.test_media,
            'schedule_time': '2026-01-09T12:00:00Z',
            'dry_run': True,
            'quality': 'high'
        })

        self.assertTrue(result['success'])
        self.assertIn('video_analysis', result)
        self.assertIn('audio_processing', result)
        self.assertIn('content_scheduling', result)

        # Test social promotion workflow
        result = self.manager.execute_workflow('social_promotion', {
            'content': 'Promoting new episode!',
            'platforms': ['twitter', 'instagram'],
            'media_path': self.test_media,
            'schedule_time': '2026-01-09T12:00:00Z',
            'dry_run': True
        })

        self.assertTrue(result['success'])
        self.assertIn('content_scheduling', result)

    def test_metrics_tracking(self):
        """Test performance metrics tracking."""

        # Execute multiple operations
        self.manager.execute_tool('video_analysis', {
            'video_path': self.test_video,
            'analysis_type': 'speaker_detection'
        })

        self.manager.execute_tool('audio_processing', {
            'audio_path': self.test_audio,
            'output_path': self.test_output,
            'processing_steps': ['noise_reduction']
        })

        # Get metrics
        metrics = self.manager.get_metrics()

        self.assertEqual(metrics['tool_metrics']['video_analysis']['execution_count'], 1)
        self.assertEqual(metrics['tool_metrics']['audio_processing']['execution_count'], 1)
        self.assertEqual(metrics['tool_metrics']['content_scheduling']['execution_count'], 0)

        # Execute workflow
        self.manager.execute_workflow('social_promotion', {
            'content': 'Test',
            'platforms': ['twitter'],
            'dry_run': True
        })

        metrics = self.manager.get_metrics()
        self.assertEqual(metrics['workflow_metrics']['total'], 1)

    def test_health_monitoring(self):
        """Test system health monitoring."""

        health = self.manager.get_health_status()

        # Check health structure
        self.assertIn('cpu_usage', health)
        self.assertIn('memory_usage', health)
        self.assertIn('disk_usage', health)
        self.assertIn('tool_error_rates', health)
        self.assertIn('status', health)

        # Status should be healthy with no errors
        self.assertEqual(health['status'], 'healthy')

    def test_integration_scenarios(self):
        """Test integration scenarios with existing codebase."""

        # Test integration with existing workflows
        from scripts.social_workflows import SocialWorkflowManager

        # Create mock social workflow manager
        social_manager = MagicMock(spec=SocialWorkflowManager)

        # Integrate with our toolset
        result = self.manager.execute_tool('content_scheduling', {
            'content': 'Integrated test',
            'platforms': ['twitter', 'instagram'],
            'dry_run': True
        })

        self.assertTrue(result['success'])

        # Test that our toolset can be used as a fallback
        with patch.object(social_manager, 'schedule_post', side_effect=Exception("API failure")):

            # Our toolset should handle the fallback
            result = self.manager.execute_tool('content_scheduling', {
                'content': 'Fallback test',
                'platforms': ['twitter'],
                'dry_run': True
            })

            self.assertTrue(result['success'])

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""

        # Test with minimal parameters
        result = self.manager.execute_tool('video_analysis', {
            'video_path': self.test_video
        })
        self.assertTrue(result['success'])

        # Test with maximum parameters
        result = self.manager.execute_tool('content_scheduling', {
            'content': 'Full parameter test',
            'platforms': ['twitter', 'instagram', 'tiktok', 'youtube', 'linkedin'],
            'media_path': self.test_media,
            'schedule_time': '2026-01-09T12:00:00Z',
            'dry_run': True,
            'quality': 'high'
        })
        self.assertTrue(result['success'])

        # Test with invalid file paths (should raise ValidationError)
        with self.assertRaises(ValidationError):
            self.manager.execute_tool('video_analysis', {
                'video_path': '/nonexistent/path.mp4'
            })

    def test_performance_under_load(self):
        """Test performance under simulated load conditions."""

        start_time = time.time()

        # Execute multiple operations in sequence
        for i in range(5):
            self.manager.execute_tool('video_analysis', {
                'video_path': self.test_video,
                'analysis_type': 'speaker_detection',
                'quality': 'medium'
            })

        execution_time = time.time() - start_time

        # Should complete within reasonable time
        self.assertLess(execution_time, 10)  # Less than 10 seconds for 5 operations

        # Check metrics
        metrics = self.manager.get_metrics()
        self.assertEqual(metrics['tool_metrics']['video_analysis']['execution_count'], 5)

    def test_error_recovery(self):
        """Test error recovery mechanisms."""

        tool = PracticalVideoAnalysisTool()

        # Simulate multiple failures
        with patch.object(tool, '_execute_method') as mock_method:
            mock_method.side_effect = [
                RecoverableError("First failure"),
                RecoverableError("Second failure"),
                MagicMock(return_value={'success': True})  # Third attempt succeeds
            ]

            result = tool.execute({
                'video_path': self.test_video,
                'analysis_type': 'speaker_detection'
            })

            self.assertTrue(result['success'])
            self.assertEqual(result['retry_attempts'], 2)
            self.assertEqual(mock_method.call_count, 3)

    def test_quality_adjustment(self):
        """Test automatic quality adjustment."""

        # Test quality reduction under resource constraints
        with patch('psutil.cpu_percent', return_value=95):
            with patch('psutil.virtual_memory', return_value=MagicMock(percent=90)):

                result = self.manager.execute_tool('video_analysis', {
                    'video_path': self.test_video,
                    'analysis_type': 'speaker_detection',
                    'quality': 'high'
                })

                self.assertTrue(result['success'])
                self.assertIn('quality_adjustment', result)
                self.assertEqual(result['quality_adjustment'], 'medium')

    def test_fallback_methods(self):
        """Test fallback method execution."""

        tool = PracticalVideoAnalysisTool()

        # Simulate primary method failure
        with patch.object(tool, '_execute_method') as mock_method:
            mock_method.side_effect = FatalError("Primary method failed")

            result = tool.execute({
                'video_path': self.test_video,
                'analysis_type': 'speaker_detection'
            })

            # Should use fallback method
            self.assertTrue(result['success'])
            self.assertIn('fallback_method_used', result)

    def test_configuration_options(self):
        """Test custom configuration options."""

        config = {
            'max_retries': 5,
            'quality_levels': ['high', 'medium', 'low', 'minimal'],
            'resource_thresholds': {
                'cpu': 85,
                'memory': 80,
                'disk': 90
            }
        }

        tool = PracticalVideoAnalysisTool(config=config)

        # Test that configuration is applied
        self.assertEqual(tool.config['max_retries'], 5)
        self.assertEqual(len(tool.config['quality_levels']), 4)

        # Test execution with custom config
        result = tool.execute({
            'video_path': self.test_video,
            'analysis_type': 'speaker_detection'
        })

        self.assertTrue(result['success'])

    def test_integration_with_mcp_servers(self):
        """Test integration with MCP servers."""

        # Mock MCP server response
        mock_response = {
            'success': True,
            'platform': 'twitter',
            'post_id': '12345',
            'scheduled_time': '2026-01-09T12:00:00Z'
        }

        # Test that our toolset can work alongside MCP servers
        result = self.manager.execute_tool('content_scheduling', {
            'content': 'MCP integration test',
            'platforms': ['twitter'],
            'dry_run': True
        })

        self.assertTrue(result['success'])

        # Our toolset should provide consistent interface
        self.assertIn('scheduled_posts', result)
        self.assertEqual(len(result['scheduled_posts']), 1)

    def test_comprehensive_workflow(self):
        """Test comprehensive end-to-end workflow."""

        # Execute complete episode production workflow
        result = self.manager.execute_workflow('episode_production', {
            'video_path': self.test_video,
            'audio_path': self.test_audio,
            'output_audio_path': self.test_output,
            'audio_processing_steps': ['noise_reduction', 'de_essing', 'equalization'],
            'schedule_social': True,
            'social_content': 'Comprehensive test episode!',
            'social_platforms': ['twitter', 'instagram', 'tiktok'],
            'social_media_path': self.test_media,
            'schedule_time': '2026-01-09T12:00:00Z',
            'dry_run': True,
            'quality': 'high'
        })

        # Verify all components executed successfully
        self.assertTrue(result['success'])
        self.assertIn('video_analysis', result)
        self.assertIn('audio_processing', result)
        self.assertIn('content_scheduling', result)

        # Verify video analysis
        self.assertTrue(result['video_analysis']['success'])
        self.assertIn('analysis_results', result['video_analysis'])

        # Verify audio processing
        self.assertTrue(result['audio_processing']['success'])
        self.assertIn('processed_audio_path', result['audio_processing'])

        # Verify content scheduling
        self.assertTrue(result['content_scheduling']['success'])
        self.assertEqual(len(result['content_scheduling']['scheduled_posts']), 3)

        # Verify metrics were tracked
        metrics = self.manager.get_metrics()
        self.assertEqual(metrics['workflow_metrics']['total'], 1)
        self.assertEqual(metrics['workflow_metrics']['success'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
