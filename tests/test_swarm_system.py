#!/usr/bin/env python3
"""Comprehensive Test Suite for Democratic AI Agent Swarm System.

This test suite covers all components of the democratic agent swarm:
- Confidence metrics and decision making
- Inter-agent communication and voting
- Observability and telemetry
- Monitoring and alerting
- Conversation logging and persistence
- Performance analysis and anomaly detection
"""

import unittest
import tempfile
import shutil
import time
import json
import threading
import logging
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from base_agent import BaseAgent, ToolBasedAgent, ConfidenceMetrics
from swarm_communication import MessageBus, VotingSystem, SwarmCoordinator, Message, VoteProposal
from swarm_observability import SwarmObservabilityManager, MessageType, A2AMessage, TelemetryCollector
from swarm_monitoring import (
    SwarmMonitor, ConversationLogger, PerformanceAnalyzer, AlertManager,
    AlertSeverity, AlertType, Alert
)


class TestConfidenceMetrics(unittest.TestCase):
    """Test confidence metrics functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.confidence = ConfidenceMetrics()

    def test_initial_confidence(self):
        """Test initial confidence values."""
        self.assertEqual(self.confidence.overall, 0.5)
        self.assertEqual(len(self.confidence.domains), 0)
        self.assertEqual(len(self.confidence.tools), 0)

    def test_recent_performance_tracking(self):
        """Test recent performance tracking."""
        # Add some performance data
        self.confidence.update_recent_performance(True)
        self.confidence.update_recent_performance(False)
        self.confidence.update_recent_performance(True)

        self.assertEqual(len(self.confidence.recent_performance), 3)
        self.assertEqual(sum(self.confidence.recent_performance), 2)  # 2 successes

    def test_overall_confidence_calculation(self):
        """Test overall confidence calculation."""
        # Setup some test data
        self.confidence.recent_performance = [True, True, False]  # 66% success
        self.confidence.total_votes = 10
        self.confidence.successful_votes = 8  # 80% voting accuracy
        self.confidence.total_communications = 20
        self.confidence.effective_communications = 18  # 90% communication effectiveness
        self.confidence.domains = {'test': 0.7}

        self.confidence.update_overall_confidence()

        # Should be weighted average of factors
        self.assertGreater(self.confidence.overall, 0.5)  # Should be higher than default

    def test_abstention_logic(self):
        """Test abstention decision logic."""
        # Low confidence should abstain
        self.confidence.overall = 0.2
        self.assertTrue(self.confidence.should_abstain())

        # High confidence should not abstain
        self.confidence.overall = 0.8
        self.assertFalse(self.confidence.should_abstain())

        # Domain-specific low confidence should abstain
        self.confidence.domains['test_domain'] = 0.1
        self.assertTrue(self.confidence.should_abstain('test_domain'))

    def test_voting_weight_calculation(self):
        """Test voting weight calculation."""
        self.confidence.overall = 0.8
        self.confidence.domains['test'] = 0.9

        # Base weight
        weight = self.confidence.get_voting_weight()
        self.assertGreaterEqual(weight, 0.1)
        self.assertLessEqual(weight, 2.0)

        # With domain boost
        weight_with_domain = self.confidence.get_voting_weight('test')
        self.assertGreater(weight_with_domain, weight)  # Should be higher


class TestBaseAgent(unittest.TestCase):
    """Test BaseAgent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.json"

        # Create test config
        test_config = {
            "agents": {
                "test_agent": {
                    "name": "Test Agent",
                    "role": "Testing",
                    "model": "gpt-4o",
                    "system_prompt": "Test prompt",
                    "tools": [
                        {"name": "test_tool", "description": "Test tool", "parameters": {}}
                    ],
                    "workflows": {}
                }
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)

        self.agent = ToolBasedAgent("test_agent", str(self.config_path))

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.agent_name, "test_agent")
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.role, "Testing")
        self.assertIsInstance(self.agent.confidence, ConfidenceMetrics)

    def test_domain_confidence_initialization(self):
        """Test domain confidence initialization based on role."""
        # Video editor should have video_editing domain confidence
        video_config = {
            "agents": {
                "video_agent": {
                    "name": "Video Agent",
                    "role": "Video production specialist",
                    "model": "gpt-4o",
                    "system_prompt": "Video prompt",
                    "tools": [],
                    "workflows": {}
                }
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(video_config, f)

        video_agent = ToolBasedAgent("video_agent", str(self.config_path))
        self.assertIn('video_editing', video_agent.confidence.domains)
        self.assertGreater(video_agent.confidence.domains['video_editing'], 0.5)

    def test_confidence_updates(self):
        """Test confidence updates after tool execution."""
        initial_confidence = self.agent.confidence.overall

        # Simulate successful tool execution
        self.agent.update_confidence_after_execution("test_tool", True)

        # Confidence should be updated
        self.assertIsInstance(self.agent.confidence.recent_performance, list)
        self.assertTrue(len(self.agent.confidence.recent_performance) > 0)

    def test_voting_methods(self):
        """Test voting-related methods."""
        # Test abstention
        self.agent.confidence.overall = 0.2  # Low confidence
        self.assertTrue(self.agent.should_abstain_from_vote())

        self.agent.confidence.overall = 0.8  # High confidence
        self.assertFalse(self.agent.should_abstain_from_vote())

        # Test voting weight
        weight = self.agent.get_voting_weight()
        self.assertGreaterEqual(weight, 0.1)
        self.assertLessEqual(weight, 2.0)

        # Test vote casting
        vote = self.agent.cast_vote("test_proposal")
        self.assertIn('decision', vote)
        self.assertIn('weight', vote)
        self.assertIn('confidence', vote)


class TestMessageBus(unittest.TestCase):
    """Test MessageBus functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_bus = MessageBus()
        self.agent = Mock()
        self.agent.agent_name = "test_agent"

    def test_agent_registration(self):
        """Test agent registration."""
        self.message_bus.register_agent(self.agent)
        self.assertIn("test_agent", self.message_bus.agents)
        self.assertIn("test_agent", self.message_bus.message_queues)

    def test_direct_messaging(self):
        """Test direct message sending."""
        self.message_bus.register_agent(self.agent)

        message = Message(
            message_id="test_msg_1",
            sender="sender",
            recipient="test_agent",
            message_type="test",
            content={"test": "data"}
        )

        success = self.message_bus.send_message(message)
        self.assertTrue(success)

        # Check message was received
        messages = self.message_bus.get_messages("test_agent")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message_id, "test_msg_1")

    def test_broadcast_messaging(self):
        """Test broadcast messaging."""
        self.message_bus.register_agent(self.agent)

        message = Message(
            message_id="test_broadcast",
            sender="sender",
            recipient="broadcast",
            message_type="announcement",
            content={"announcement": "test"}
        )

        success = self.message_bus.send_message(message)
        self.assertTrue(success)

        messages = self.message_bus.get_messages("test_agent")
        self.assertEqual(len(messages), 1)

    def test_channel_messaging(self):
        """Test channel-based messaging."""
        self.message_bus.register_agent(self.agent)
        self.message_bus.subscribe_to_channel("test_agent", "test_channel")

        message = Message(
            message_id="test_channel_msg",
            sender="sender",
            recipient="channel:test_channel",
            message_type="channel_msg",
            content={"channel_data": "test"}
        )

        success = self.message_bus.send_message(message)
        self.assertTrue(success)

        messages = self.message_bus.get_messages("test_agent")
        self.assertEqual(len(messages), 1)


class TestVotingSystem(unittest.TestCase):
    """Test VotingSystem functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_bus = MessageBus()
        self.voting_system = VotingSystem(self.message_bus)

    def test_proposal_creation(self):
        """Test voting proposal creation."""
        proposal_id = self.voting_system.create_proposal(
            proposer="test_proposer",
            title="Test Proposal",
            description="Test voting proposal",
            options=["option_a", "option_b"],
            context="test_context"
        )

        self.assertIn(proposal_id, self.voting_system.proposals)
        proposal = self.voting_system.proposals[proposal_id]
        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(len(proposal.options), 2)

    def test_vote_casting(self):
        """Test vote casting."""
        # Create proposal
        proposal_id = self.voting_system.create_proposal(
            "proposer", "Test", "Description", ["yes", "no"]
        )

        # Create mock agent
        agent = Mock()
        agent.agent_name = "voter_agent"
        agent.cast_vote.return_value = {
            'decision': 'yes',
            'weight': 1.0,
            'confidence': 0.8
        }

        # Cast vote
        success = self.voting_system.cast_vote(proposal_id, agent, "yes")
        self.assertTrue(success)

        # Check vote was recorded
        proposal = self.voting_system.proposals[proposal_id]
        self.assertIn("voter_agent", proposal.votes)
        self.assertEqual(proposal.votes["voter_agent"]['decision'], 'yes')

    def test_vote_summary(self):
        """Test vote summary calculation."""
        proposal = VoteProposal(
            proposal_id="test",
            proposer="test",
            title="Test",
            description="Test",
            options=["yes", "no"]
        )

        # Add some votes
        proposal.add_vote("agent1", {'decision': 'yes', 'weight': 1.0})
        proposal.add_vote("agent2", {'decision': 'yes', 'weight': 1.5})
        proposal.add_vote("agent3", {'decision': 'no', 'weight': 1.0})

        summary = proposal.get_vote_summary()

        self.assertEqual(summary['total_votes'], 3)
        self.assertAlmostEqual(summary['total_weight'], 3.5)
        self.assertIn('yes', summary['results'])
        self.assertIn('no', summary['results'])


class TestConversationLogger(unittest.TestCase):
    """Test ConversationLogger functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = str(Path(self.temp_dir) / "test_conversations.db")
        self.logger = ConversationLogger(self.db_path)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_message_logging(self):
        """Test message logging."""
        message = A2AMessage(
            id="test_msg_1",
            sender="agent_a",
            recipient="agent_b",
            message_type=MessageType.AGENT_STATUS,
            content={"status": "active"}
        )

        self.logger.log_message(message)

        # Check message was logged
        conversations = self.logger.get_conversation_history("test_msg_1")
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['sender'], "agent_a")

    def test_vote_logging(self):
        """Test vote logging."""
        vote = {
            'decision': 'approve',
            'weight': 1.5,
            'confidence': 0.8
        }

        self.logger.log_vote("proposal_1", "agent_1", vote)

        # Could add verification query here if needed

    def test_task_logging(self):
        """Test task logging."""
        self.logger.log_task("task_1", "agent_1", "test_type", "completed", True, {"result": "success"})

        # Could add verification query here if needed

    def test_system_metrics(self):
        """Test system metrics retrieval."""
        metrics = self.logger.get_system_metrics(hours=1)
        self.assertIn('total_messages', metrics)
        self.assertIn('task_completion', metrics)


class TestAlertManager(unittest.TestCase):
    """Test AlertManager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = str(Path(self.temp_dir) / "test_alerts.db")
        self.conversation_logger = ConversationLogger(self.db_path)
        self.alert_manager = AlertManager(self.conversation_logger)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_alert_creation(self):
        """Test alert creation."""
        alert_id = self.alert_manager.raise_alert(
            AlertSeverity.ERROR,
            AlertType.AGENT_FAILURE,
            "Test Alert",
            "This is a test alert",
            agent_name="test_agent",
            metadata={"test": "data"}
        )

        self.assertIn(alert_id, self.alert_manager.active_alerts)
        alert = self.alert_manager.active_alerts[alert_id]
        self.assertEqual(alert.title, "Test Alert")
        self.assertEqual(alert.severity, AlertSeverity.ERROR)

    def test_alert_resolution(self):
        """Test alert resolution."""
        alert_id = self.alert_manager.raise_alert(
            AlertSeverity.WARNING,
            AlertType.COMMUNICATION_ERROR,
            "Test Alert",
            "Test description"
        )

        # Resolve alert
        success = self.alert_manager.resolve_alert(alert_id, "Issue resolved")
        self.assertTrue(success)

        # Check alert is resolved
        self.assertNotIn(alert_id, self.alert_manager.active_alerts)

    def test_alert_handlers(self):
        """Test alert handler registration and execution."""
        handler_called = []

        def test_handler(alert):
            handler_called.append(alert.title)

        self.alert_manager.register_alert_handler(AlertType.AGENT_FAILURE, test_handler)

        # Raise alert
        self.alert_manager.raise_alert(
            AlertSeverity.CRITICAL,
            AlertType.AGENT_FAILURE,
            "Handler Test",
            "Testing alert handlers"
        )

        # Check handler was called
        self.assertEqual(len(handler_called), 1)
        self.assertEqual(handler_called[0], "Handler Test")

    def test_alert_filtering(self):
        """Test alert filtering by severity."""
        # Create alerts of different severities
        self.alert_manager.raise_alert(
            AlertSeverity.INFO, AlertType.AGENT_FAILURE, "Info Alert", "Info"
        )
        self.alert_manager.raise_alert(
            AlertSeverity.ERROR, AlertType.AGENT_FAILURE, "Error Alert", "Error"
        )

        # Get all alerts
        all_alerts = self.alert_manager.get_active_alerts()
        self.assertEqual(len(all_alerts), 2)

        # Get only error alerts
        error_alerts = self.alert_manager.get_active_alerts(AlertSeverity.ERROR)
        self.assertEqual(len(error_alerts), 1)
        self.assertEqual(error_alerts[0].title, "Error Alert")


class TestSwarmMonitor(unittest.TestCase):
    """Test SwarmMonitor functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.observability = SwarmObservabilityManager()
        self.monitor = SwarmMonitor(self.observability)

    def test_monitor_initialization(self):
        """Test monitor initialization."""
        self.assertIsInstance(self.monitor.conversation_logger, ConversationLogger)
        self.assertIsInstance(self.monitor.performance_analyzer, PerformanceAnalyzer)
        self.assertIsInstance(self.monitor.alert_manager, AlertManager)

    def test_monitoring_start_stop(self):
        """Test monitoring start/stop."""
        self.assertFalse(self.monitor.monitoring_active)

        self.monitor.start_monitoring()
        self.assertTrue(self.monitor.monitoring_active)

        self.monitor.stop_monitoring()
        self.assertFalse(self.monitor.monitoring_active)

    def test_monitoring_status(self):
        """Test monitoring status retrieval."""
        status = self.monitor.get_monitoring_status()

        required_keys = [
            'monitoring_active', 'conversation_logs', 'active_alerts',
            'performance_analysis', 'system_metrics', 'alert_history'
        ]

        for key in required_keys:
            self.assertIn(key, status)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete swarm system."""

    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "integration_config.json"

        # Create integration config
        integration_config = {
            "agents": {
                "integration_agent_1": {
                    "name": "Integration Agent 1",
                    "role": "Video production specialist",
                    "model": "gpt-4o",
                    "system_prompt": "Integration test agent",
                    "tools": [
                        {"name": "video_tool", "description": "Video processing tool", "parameters": {}}
                    ],
                    "workflows": {}
                },
                "integration_agent_2": {
                    "name": "Integration Agent 2",
                    "role": "Audio production specialist",
                    "model": "gpt-4o",
                    "system_prompt": "Integration test agent 2",
                    "tools": [],
                    "workflows": {}
                }
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(integration_config, f)

    def tearDown(self):
        """Clean up integration test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_full_agent_lifecycle(self):
        """Test complete agent lifecycle with monitoring."""
        # Create agents
        agent1 = ToolBasedAgent("integration_agent_1", str(self.config_path))
        agent2 = ToolBasedAgent("integration_agent_2", str(self.config_path))

        # Initialize observability
        observability = SwarmObservabilityManager()
        monitor = SwarmMonitor(observability)

        # Register agents
        observability.register_agent(agent1)
        observability.register_agent(agent2)

        # Start monitoring
        monitor.start_monitoring()

        try:
            # Test communication
            message = A2AMessage(
                sender="integration_agent_1",
                recipient="integration_agent_2",
                message_type=MessageType.AGENT_STATUS,
                content={"status": "testing"}
            )

            success = observability.a2a_handler.send_a2a_message(message)
            self.assertTrue(success)

            # Test voting
            proposal_id = observability.create_vote_proposal(
                "integration_agent_1",
                "Integration Test Proposal",
                "Test democratic voting",
                ["approve", "deny"]
            )

            # Cast votes
            observability.voting_system.cast_vote(proposal_id, agent1, "approve")
            observability.voting_system.cast_vote(proposal_id, agent2, "approve")

            # Check proposal status
            status = observability.voting_system.get_proposal_status(proposal_id)
            self.assertIsNotNone(status)

            # Test task assignment
            task = {
                'id': 'integration_task',
                'type': 'video_processing',
                'description': 'Test task',
                'context': 'video_editing'
            }

            assigned_agent = observability.assign_task(task)
            self.assertIsNotNone(assigned_agent)

            # Test monitoring status
            monitoring_status = monitor.get_monitoring_status()
            self.assertIn('active_alerts', monitoring_status)
            self.assertIn('system_metrics', monitoring_status)

        finally:
            # Cleanup
            monitor.stop_monitoring()


if __name__ == '__main__':
    # Setup logging for tests
    logging.basicConfig(
        level=logging.WARNING,  # Reduce log noise during tests
        format='%(levelname)s - %(name)s - %(message)s'
    )

    # Run tests
    unittest.main(verbosity=2)
