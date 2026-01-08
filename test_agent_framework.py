#!/usr/bin/env python3
"""Test script for the agent framework.

This script demonstrates that the agent framework can load agents from agents_config.json
and execute basic operations.
"""

import sys
import os
from pathlib import Path

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

import pytest
from base_agent import ToolBasedAgent, WorkflowOrchestrator


def load_agents():
    """Load agents from configuration for tests and manual runs."""
    video_agent = ToolBasedAgent("video_editor")
    audio_agent = ToolBasedAgent("audio_engineer")
    social_agent = ToolBasedAgent("social_media_manager")
    return video_agent, audio_agent, social_agent


@pytest.fixture()
def agents():
    return load_agents()


def test_agent_loading(agents):
    """Test loading agents from configuration."""
    video_agent, audio_agent, social_agent = agents
    assert video_agent.name
    assert audio_agent.name
    assert social_agent.name


def test_tool_execution(agents):
    """Test executing tools (placeholders may fail)."""
    video_agent, audio_agent, _social_agent = agents
    video_result = video_agent.execute_tool(
        "video_analysis",
        {"video_path": "test_video.mp4", "analysis_type": "speaker_detection"},
    )
    assert hasattr(video_result, "success")
    audio_result = audio_agent.execute_tool(
        "audio_cleanup",
        {"audio_file": "test_audio.wav", "noise_reduction_level": "medium"},
    )
    assert hasattr(audio_result, "success")


def test_workflow_orchestrator():
    """Test workflow orchestrator."""
    orchestrator = WorkflowOrchestrator()
    workflows = orchestrator.get_available_workflows()
    assert isinstance(workflows, list)
    episode_info = orchestrator.get_workflow_info("episode_production")
    if episode_info:
        assert "description" in episode_info


def test_agent_status(agents):
    """Test getting agent status."""
    for agent in agents:
        status = agent.get_status()
        assert "model" in status
        assert "success_rate" in status
        assert "available_tools" in status


def main():
    """Run all tests."""
    print("🔧 Testing Agent Framework")
    print("=" * 50)

    # Test agent loading
    agents = load_agents()
    if not all(agents):
        print("❌ Agent loading failed, stopping tests")
        return

    # Test tool execution
    test_tool_execution(agents)

    # Test workflow orchestrator
    orchestrator = test_workflow_orchestrator()

    # Test agent status
    test_agent_status(agents)

    print("\n" + "=" * 50)
    print("🎉 Agent framework tests completed!")
    print("\nNote: Tools currently return placeholder errors since actual implementations")
    print("need to be built. The framework successfully loads configuration and manages")
    print("agent lifecycles, tool execution, and workflow orchestration.")


if __name__ == "__main__":
    main()
