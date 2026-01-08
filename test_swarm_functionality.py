#!/usr/bin/env python3
"""Test suite for democratic agent swarm functionality."""

import unittest
import time
from unittest.mock import Mock, patch

# Add agents directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from swarm_communication import MessageBus, VotingSystem, VoteProposal, SwarmCoordinator
from swarm_observability import SwarmObservabilityManager
from base_agent import ToolBasedAgent


class TestSwarmCommunication(unittest.TestCase):
    """Test swarm communication infrastructure."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_bus = MessageBus()
        self.voting_system = VotingSystem(self.message_bus)
        self.coordinator = SwarmCoordinator(self.message_bus, self.voting_system)

    def test_message_bus_registration(self):
        """Test agent registration with message bus."""
        # Create mock agent
        mock_agent = Mock()
        mock_agent.agent_name = "test_agent"

        self.message_bus.register_agent(mock_agent)
        self.assertIn("test_agent", self.message_bus.agents)
        self.assertIn("test_agent", self.message_bus.message_queues)

    def test_message_sending(self):
        """Test message sending between agents."""
        # Register test agents
        agent1 = Mock()
        agent1.agent_name = "agent1"
        agent2 = Mock()
        agent2.agent_name = "agent2"

        self.message_bus.register_agent(agent1)
        self.message_bus.register_agent(agent2)

        # Send direct message
        from swarm_communication import Message
        message = Message(
            message_id="test_msg_1",
            sender="agent1",
            recipient="agent2",
            message_type="test",
            content={"test": "data"}
        )

        success = self.message_bus.send_message(message)
        self.assertTrue(success)

        # Check message was received
        messages = self.message_bus.get_messages("agent2")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content["test"], "data")

    def test_broadcast_messaging(self):
        """Test broadcast message functionality."""
        # Register multiple agents
        for i in range(3):
            agent = Mock()
            agent.agent_name = f"agent{i}"
            self.message_bus.register_agent(agent)

        # Send broadcast message
        from swarm_communication import Message
        message = Message(
            message_id="broadcast_test",
            sender="coordinator",
            recipient="broadcast",
            message_type="announcement",
            content={"announcement": "test broadcast"}
        )

        success = self.message_bus.send_message(message)
        self.assertTrue(success)

        # Check all agents received the message
        total_messages = 0
        for agent_name in ["agent0", "agent1", "agent2"]:
            messages = self.message_bus.get_messages(agent_name)
            total_messages += len(messages)

        self.assertEqual(total_messages, 3)


class TestVotingSystem(unittest.TestCase):
    """Test democratic voting system."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_bus = MessageBus()
        self.voting_system = VotingSystem(self.message_bus)

        # Create and register mock agents
        self.mock_agents = {}
        for name in ["agent1", "agent2", "agent3"]:
            agent = Mock()
            agent.agent_name = name
            agent.cast_vote.return_value = {
                'decision': 'yes',  # Will be set appropriately per test
                'weight': 1.0,
                'confidence': 0.8
            }
            self.mock_agents[name] = agent
            self.message_bus.register_agent(agent)

    def test_proposal_creation(self):
        """Test creating a voting proposal."""
        proposal_id = self.voting_system.create_proposal(
            proposer="test_proposer",
            title="Test Proposal",
            description="A test voting proposal",
            options=["option1", "option2", "option3"],
            context="testing"
        )

        self.assertIsNotNone(proposal_id)
        self.assertIn(proposal_id, self.voting_system.proposals)

        proposal = self.voting_system.proposals[proposal_id]
        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(len(proposal.options), 3)

    def test_vote_casting(self):
        """Test casting votes on a proposal."""
        # Create proposal
        proposal_id = self.voting_system.create_proposal(
            "proposer", "Test Vote", "Test description",
            ["yes", "no"], "test"
        )

        # Cast votes
        for agent_name, agent in self.mock_agents.items():
            success = self.voting_system.cast_vote(proposal_id, agent, "yes")
            self.assertTrue(success)

        # Check votes were recorded
        proposal = self.voting_system.proposals[proposal_id]
        self.assertEqual(len(proposal.votes), 3)

        summary = proposal.get_vote_summary()
        self.assertEqual(summary['total_votes'], 3)
        self.assertEqual(summary['results']['yes']['weight'], 3.0)

    def test_vote_validation(self):
        """Test vote validation."""
        proposal_id = self.voting_system.create_proposal(
            "proposer", "Test", "Test", ["valid_option"], "test"
        )

        agent = self.mock_agents["agent1"]

        # Test invalid option
        agent.cast_vote.return_value = {
            'decision': 'invalid_option',
            'weight': 1.0,
            'confidence': 0.8
        }

        success = self.voting_system.cast_vote(proposal_id, agent, "invalid_option")
        self.assertFalse(success)

        # Check validation error was recorded
        proposal = self.voting_system.proposals[proposal_id]
        self.assertTrue(len(proposal.validation_errors) > 0)

    def test_attendance_tracking(self):
        """Test attendance tracking in proposals."""
        proposal_id = self.voting_system.create_proposal(
            "proposer", "Test", "Test", ["option1"], "test"
        )

        proposal = self.voting_system.proposals[proposal_id]

        # Record attendance
        proposal.record_attendance("agent1", "present")
        proposal.record_attendance("agent2", "absent")

        attendance_report = proposal.get_attendance_report()
        self.assertEqual(attendance_report['total_registered'], 2)
        self.assertEqual(attendance_report['voted'], 0)  # No votes cast yet
        self.assertEqual(attendance_report['absent'], 1)

    def test_conversation_logging(self):
        """Test conversation logging."""
        proposal_id = self.voting_system.create_proposal(
            "proposer", "Test", "Test", ["option1"], "test"
        )

        success = self.voting_system.log_conversation(
            proposal_id, "agent1", "I think option1 is best", "discussion"
        )
        self.assertTrue(success)

        proposal = self.voting_system.proposals[proposal_id]
        conversation_summary = proposal.get_conversation_summary()
        self.assertEqual(conversation_summary['total_messages'], 1)
        self.assertEqual(conversation_summary['message_types']['discussion'], 1)


class TestSwarmCoordinator(unittest.TestCase):
    """Test swarm coordinator functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.message_bus = MessageBus()
        self.voting_system = VotingSystem(self.message_bus)
        self.coordinator = SwarmCoordinator(self.message_bus, self.voting_system)

        # Create mock agents
        self.mock_agents = {}
        for name in ["worker1", "worker2"]:
            agent = Mock()
            agent.agent_name = name
            # Mock confidence as an object with attributes
            agent.confidence = Mock()
            agent.confidence.overall = 0.8
            agent.confidence.get_domain_confidence.return_value = 0.7
            agent.confidence.get_tool_confidence.return_value = 0.6
            agent.get_available_tools.return_value = ["tool1", "tool2"]
            self.mock_agents[name] = agent
            self.message_bus.register_agent(agent)

    def test_task_assignment(self):
        """Test task assignment to agents."""
        task = {
            'id': 'test_task_1',
            'type': 'general',
            'context': 'testing'
        }

        assigned_agent = self.coordinator.assign_task(task)
        self.assertIsNotNone(assigned_agent)
        self.assertIn(assigned_agent, self.mock_agents)

        # Check task was recorded
        self.assertIn('test_task_1', self.coordinator.active_tasks)
        self.assertEqual(self.coordinator.task_assignments['test_task_1'], assigned_agent)

    def test_task_completion(self):
        """Test task completion reporting."""
        # First assign a task
        task = {'id': 'completion_test', 'type': 'test'}
        assigned_agent = self.coordinator.assign_task(task)
        self.assertIsNotNone(assigned_agent)

        # Report completion
        self.coordinator.report_task_completion('completion_test', assigned_agent, True, {'result': 'success'})

        # Check task moved to completed
        self.assertNotIn('completion_test', self.coordinator.active_tasks)
        self.assertIn('completion_test', self.coordinator.completed_tasks)

        completed_task = self.coordinator.completed_tasks['completion_test']
        self.assertTrue(completed_task['success'])
        self.assertEqual(completed_task['result'], {'result': 'success'})

    def test_swarm_status(self):
        """Test swarm status reporting."""
        status = self.coordinator.get_swarm_status()

        required_keys = ['active_tasks', 'completed_tasks', 'success_rate', 'runtime', 'agents']
        for key in required_keys:
            self.assertIn(key, status)

        self.assertEqual(status['agents'], 2)  # Two mock agents


class TestSwarmObservability(unittest.TestCase):
    """Test swarm observability features."""

    def setUp(self):
        """Set up test fixtures."""
        self.observability = SwarmObservabilityManager()

        # Create mock agent
        self.mock_agent = Mock()
        self.mock_agent.agent_name = "test_agent"
        self.mock_agent.name = "Test Agent"
        self.mock_agent.role = "testing"
        # Mock confidence
        self.mock_agent.confidence = Mock()
        self.mock_agent.confidence.overall = 0.8
        self.mock_agent.confidence.get_domain_confidence.return_value = 0.7
        self.mock_agent.confidence.get_tool_confidence.return_value = 0.6
        self.mock_agent.get_available_tools.return_value = ["test_tool"]

    def test_agent_registration(self):
        """Test agent registration with observability."""
        self.observability.register_agent(self.mock_agent)

        # Check agent was registered
        self.assertIn("test_agent", self.observability.message_bus.agents)
        self.assertIn("test_agent", self.observability.a2a_handler.agent_registry)

    def test_vote_proposal_creation(self):
        """Test creating voting proposals through observability."""
        proposal_id = self.observability.create_vote_proposal(
            "test_proposer",
            "Test Proposal",
            "Test description",
            ["option1", "option2"]
        )

        self.assertIsNotNone(proposal_id)
        self.assertIn(proposal_id, self.observability.voting_system.proposals)

    def test_task_assignment_observability(self):
        """Test task assignment with observability."""
        # Register an agent first
        self.observability.register_agent(self.mock_agent)

        task = {'id': 'obs_test_task', 'type': 'test'}
        assigned_agent = self.observability.assign_task(task)

        # Should assign to our registered agent
        self.assertEqual(assigned_agent, "test_agent")

    def test_comprehensive_status(self):
        """Test comprehensive status reporting."""
        status = self.observability.get_comprehensive_status()

        required_sections = ['telemetry', 'message_bus', 'voting_system', 'coordinator', 'a2a_protocol']
        for section in required_sections:
            self.assertIn(section, status)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)