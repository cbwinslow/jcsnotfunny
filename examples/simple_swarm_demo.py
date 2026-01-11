#!/usr/bin/env python3
"""
Simple Pydantic AI Democratic Swarm Demo

A basic demonstration of the core features without complex dependencies.
Perfect for quick testing and understanding the fundamental concepts.

Usage:
    python examples/simple_swarm_demo.py

Requirements:
    - OpenAI API key in OPENAI_API_KEY environment variable
    - Basic Python dependencies installed
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the agents package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent


async def basic_swarm_demo():
    """Demonstrate basic swarm functionality."""
    print("=== Pydantic AI Swarm - Basic Demo ===")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Please set OPENAI_API_KEY environment variable")
        return 1

    try:
        # Create swarm
        swarm = PydanticAISwarmOrchestrator("BasicDemo")

        # Create and register agent
        agent = PydanticVideoEditorAgent("demo_agent")
        await swarm.register_agent(agent)

        print(f"Created swarm with 1 agent: {agent.agent_name}")

        # Start swarm
        await swarm.start_swarm()
        print("Swarm started successfully")

        # Execute simple task
        result = await swarm.execute_task(
            "Describe what a video editor does",
            {"domain": "video_editing"}
        )

        if result.success:
            print(f"SUCCESS: Task completed by {result.agent_name}")
            print(f"Response length: {len(str(result.data))} characters")
        else:
            print(f"FAILED: {result.error}")

        # Show basic health
        health = await swarm.analyze_swarm_health()
        print(".2f"
        # Clean shutdown
        await swarm.stop_swarm()
        print("Demo completed successfully")

        return 0

    except Exception as e:
        print(f"Demo failed: {e}")
        return 1


async def multi_agent_demo():
    """Demonstrate multiple agents working together."""
    print("\n=== Multi-Agent Demo ===")

    try:
        # Create swarm with multiple agents
        swarm = PydanticAISwarmOrchestrator("MultiAgentDemo")

        # Create multiple agents
        agents = []
        for i in range(3):
            agent = PydanticVideoEditorAgent(f"agent_{i+1}")
            agents.append(agent)
            await swarm.register_agent(agent)

        print(f"Created swarm with {len(agents)} agents")

        # Start swarm
        await swarm.start_swarm()

        # Execute multiple tasks
        tasks = [
            "Explain video editing basics",
            "Describe color grading techniques",
            "What is multi-camera editing?"
        ]

        for i, task in enumerate(tasks, 1):
            print(f"\nTask {i}: {task}")
            result = await swarm.execute_task(task, {"domain": "video_editing"})

            if result.success:
                print(f"  Completed by: {result.agent_name}")
            else:
                print(f"  Failed: {result.error}")

        # Show final status
        status = await swarm.get_swarm_status()
        print("
Final Status:"        print(f"  Active agents: {status['agents']['active']}")
        print(f"  Tasks processed: {status['tasks']['total_processed']}")

        await swarm.stop_swarm()
        print("Multi-agent demo completed")

        return 0

    except Exception as e:
        print(f"Multi-agent demo failed: {e}")
        return 1


async def error_handling_demo():
    """Demonstrate error handling and recovery."""
    print("\n=== Error Handling Demo ===")

    try:
        swarm = PydanticAISwarmOrchestrator("ErrorDemo")
        agent = PydanticVideoEditorAgent("error_test_agent")

        await swarm.register_agent(agent)
        await swarm.start_swarm()

        # Test with invalid task (should handle gracefully)
        result = await swarm.execute_task("", {})  # Empty task

        if not result.success:
            print("SUCCESS: Error handled correctly")
            print(f"Error message: {result.error[:100]}...")
        else:
            print("UNEXPECTED: Empty task should have failed")

        await swarm.stop_swarm()
        print("Error handling demo completed")

        return 0

    except Exception as e:
        print(f"Error handling demo failed: {e}")
        return 1


async def main():
    """Run all demo scenarios."""
    print("Pydantic AI Democratic Swarm - Simple Demo Suite")
    print("=" * 55)

    demos = [
        ("Basic Swarm", basic_swarm_demo),
        ("Multi-Agent", multi_agent_demo),
        ("Error Handling", error_handling_demo),
    ]

    results = []
    for name, demo_func in demos:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            result = await demo_func()
            results.append(result == 0)
            status = "PASSED" if result == 0 else "FAILED"
            print(f"{name}: {status}")
        except Exception as e:
            print(f"{name}: FAILED - {e}")
            results.append(False)

    print("
=== Demo Results ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("All demos completed successfully!")
        return 0
    else:
        print("Some demos failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
