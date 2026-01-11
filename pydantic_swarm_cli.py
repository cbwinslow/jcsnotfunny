#!/usr/bin/env python3
"""
Pydantic AI Democratic Swarm - Command Line Interface

A comprehensive CLI for managing and interacting with Pydantic AI Democratic Swarms.

Usage:
    python pydantic_swarm_cli.py [command] [options]

Commands:
    start       Start a swarm with specified configuration
    stop        Stop a running swarm
    status      Show swarm status and health
    execute     Execute a task through the swarm
    monitor     Start monitoring mode with real-time updates
    diagnose    Run diagnostic checks and show recommendations
    demo        Run demonstration scenarios
    help        Show this help message

Examples:
    # Start a basic swarm
    python pydantic_swarm_cli.py start --name MySwarm --agents 3

    # Execute a task
    python pydantic_swarm_cli.py execute "Analyze this video" --domain video_editing

    # Check status
    python pydantic_swarm_cli.py status

    # Run diagnostics
    python pydantic_swarm_cli.py diagnose

    # Run demo
    python pydantic_swarm_cli.py demo --scenario basic

Environment Variables:
    OPENAI_API_KEY          Your OpenAI API key (required)
    PYDANTIC_AI_LOG_LEVEL   Logging level (DEBUG, INFO, WARNING, ERROR)
    SWARM_NAME             Default swarm name
    SWARM_MAX_AGENTS       Maximum agents per swarm

For more information, see the documentation at:
https://github.com/your-org/pydantic-ai-swarm
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=getattr(logging, os.getenv("PYDANTIC_AI_LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add agents package to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
    from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent
    from agents.diagnostic_system import SwarmDiagnosticSystem
except ImportError as e:
    print(f"ERROR: Failed to import required modules: {e}")
    print("Please ensure you have installed the package correctly.")
    sys.exit(1)


class SwarmCLI:
    """Command Line Interface for Pydantic AI Swarm."""

    def __init__(self):
        self.swarm: Optional[PydanticAISwarmOrchestrator] = None
        self.diagnostics: Optional[SwarmDiagnosticSystem] = None

    async def start_swarm(self, name: str, agent_count: int = 1) -> bool:
        """Start a swarm with specified number of agents."""
        try:
            print(f"Starting swarm '{name}' with {agent_count} agents...")

            # Create swarm
            self.swarm = PydanticAISwarmOrchestrator(name)

            # Create and register agents
            for i in range(agent_count):
                agent = PydanticVideoEditorAgent(f"agent_{i+1}")
                await self.swarm.register_agent(agent)
                print(f"  Registered agent: {agent.agent_name}")

            # Start the swarm
            await self.swarm.start_swarm()
            print(f"Swarm '{name}' started successfully!")

            # Initialize diagnostics
            self.diagnostics = SwarmDiagnosticSystem(self.swarm)
            await self.diagnostics.start_monitoring()

            return True

        except Exception as e:
            print(f"Failed to start swarm: {e}")
            return False

    async def stop_swarm(self) -> bool:
        """Stop the current swarm."""
        if not self.swarm:
            print("No active swarm to stop")
            return False

        try:
            print("Stopping swarm...")
            await self.diagnostics.stop_monitoring() if self.diagnostics else None
            await self.swarm.stop_swarm()
            print("Swarm stopped successfully")
            return True
        except Exception as e:
            print(f"Failed to stop swarm: {e}")
            return False

    async def show_status(self) -> bool:
        """Show swarm status and health."""
        if not self.swarm:
            print("No active swarm")
            return False

        try:
            # Get status
            status = await self.swarm.get_swarm_status()
            health = await self.swarm.analyze_swarm_health()

            print("=== Swarm Status ===")
            print(f"Name: {status['swarm_name']}")
            print(f"Active: {status['is_active']}")
            print(f"Uptime: {status['uptime_seconds']:.1f} seconds")
            print(f"Agents: {status['agents']['active']}/{status['agents']['total']}")
            print(f"Tasks Processed: {status['tasks']['total_processed']}")
            print(".2f"
            print("
=== Health Analysis ==="            print(".2f"            print(f"Status: {health['health_status']}")

            if health.get('critical_issues'):
                print("
Critical Issues:"                for issue in health['critical_issues']:
                    print(f"  - {issue['title']}: {issue['description']}")

            if health.get('recommendations'):
                print("
Recommendations:"                for rec in health['recommendations'][:3]:
                    print(f"  - {rec['title']}")

            return True

        except Exception as e:
            print(f"Failed to get status: {e}")
            return False

    async def execute_task(self, task: str, domain: str = "general", priority: str = "normal") -> bool:
        """Execute a task through the swarm."""
        if not self.swarm:
            print("No active swarm")
            return False

        try:
            print(f"Executing task: {task[:50]}{'...' if len(task) > 50 else ''}")

            result = await self.swarm.execute_task(
                task,
                {
                    "domain": domain,
                    "priority": priority
                }
            )

            if result.success:
                print("SUCCESS: Task completed")
                print(f"Agent: {result.agent_name}")
                print(".2f"                if result.data:
                    print(f"Response: {str(result.data)[:200]}{'...' if len(str(result.data)) > 200 else ''}")
            else:
                print("FAILED: Task execution failed")
                print(f"Error: {result.error}")

            return result.success

        except Exception as e:
            print(f"Task execution failed: {e}")
            return False

    async def run_diagnostics(self) -> bool:
        """Run comprehensive diagnostics."""
        if not self.swarm or not self.diagnostics:
            print("No active swarm with diagnostics")
            return False

        try:
            print("Running diagnostic checks...")

            issues = await self.diagnostics.run_diagnostics()

            print(f"\nFound {len(issues)} diagnostic issues:")

            for issue in issues:
                severity_icon = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢",
                    "info": "ℹ️"
                }.get(issue.severity, "❓")

                print(f"\n{severity_icon} {issue.severity.upper()}: {issue.title}")
                print(f"   {issue.description}")

                if issue.solutions:
                    print("   Solutions:")
                    for solution in issue.solutions[:2]:  # Show first 2 solutions
                        automated = " (automated)" if solution.get("automated") else ""
                        print(f"     - {solution['description']}{automated}")

            if not issues:
                print("✅ No diagnostic issues found!")

            return True

        except Exception as e:
            print(f"Diagnostics failed: {e}")
            return False

    async def run_demo(self, scenario: str = "basic") -> bool:
        """Run demonstration scenarios."""
        print(f"Running {scenario} demo...")

        try:
            if scenario == "basic":
                return await self._run_basic_demo()
            elif scenario == "multi-agent":
                return await self._run_multi_agent_demo()
            elif scenario == "error-handling":
                return await self._run_error_demo()
            else:
                print(f"Unknown demo scenario: {scenario}")
                return False

        except Exception as e:
            print(f"Demo failed: {e}")
            return False

    async def _run_basic_demo(self) -> bool:
        """Run basic functionality demo."""
        # Start swarm
        if not await self.start_swarm("BasicDemo", 1):
            return False

        # Execute tasks
        tasks = [
            "Explain what video editing involves",
            "Describe color grading in video production"
        ]

        for task in tasks:
            await self.execute_task(task, "video_editing")

        # Show status
        await self.show_status()

        # Stop swarm
        await self.stop_swarm()
        return True

    async def _run_multi_agent_demo(self) -> bool:
        """Run multi-agent coordination demo."""
        # Start swarm with multiple agents
        if not await self.start_swarm("MultiAgentDemo", 3):
            return False

        # Execute multiple tasks
        tasks = [
            ("Analyze video engagement patterns", "video_editing"),
            ("Optimize content for social media", "content_creation"),
            ("Generate video editing workflow", "video_editing")
        ]

        for task, domain in tasks:
            await self.execute_task(task, domain)

        # Show final status
        await self.show_status()
        await self.stop_swarm()
        return True

    async def _run_error_demo(self) -> bool:
        """Run error handling demo."""
        if not await self.start_swarm("ErrorDemo", 1):
            return False

        print("Testing error scenarios...")

        # Test with invalid task
        await self.execute_task("", "video_editing")  # Empty task

        # Test with invalid domain
        await self.execute_task("Test task", "invalid_domain")

        # Show that swarm remains operational
        print("\nSwarm error resilience test:")
        status = await self.swarm.get_swarm_status()
        print(f"Swarm still active: {status['is_active']}")
        print(f"Tasks processed: {status['tasks']['total_processed']}")

        await self.stop_swarm()
        return True


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Pydantic AI Democratic Swarm CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a swarm")
    start_parser.add_argument("--name", default="PydanticSwarm", help="Swarm name")
    start_parser.add_argument("--agents", type=int, default=1, help="Number of agents")

    # Stop command
    subparsers.add_parser("stop", help="Stop the current swarm")

    # Status command
    subparsers.add_parser("status", help="Show swarm status")

    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute a task")
    execute_parser.add_argument("task", help="Task description")
    execute_parser.add_argument("--domain", default="general", help="Task domain")
    execute_parser.add_argument("--priority", default="normal",
                               choices=["low", "normal", "high"], help="Task priority")

    # Monitor command
    subparsers.add_parser("monitor", help="Start monitoring mode")

    # Diagnose command
    subparsers.add_parser("diagnose", help="Run diagnostics")

    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demonstration")
    demo_parser.add_argument("--scenario", default="basic",
                           choices=["basic", "multi-agent", "error-handling"],
                           help="Demo scenario to run")

    # Help command
    subparsers.add_parser("help", help="Show help")

    return parser


async def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle help
    if args.command == "help" or not args.command:
        parser.print_help()
        return 0

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable is required")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        return 1

    # Create CLI instance
    cli = SwarmCLI()

    try:
        # Execute command
        if args.command == "start":
            success = await cli.start_swarm(args.name, args.agents)
        elif args.command == "stop":
            success = await cli.stop_swarm()
        elif args.command == "status":
            success = await cli.show_status()
        elif args.command == "execute":
            success = await cli.execute_task(args.task, args.domain, args.priority)
        elif args.command == "diagnose":
            success = await cli.run_diagnostics()
        elif args.command == "demo":
            success = await cli.run_demo(args.scenario)
        elif args.command == "monitor":
            print("Monitoring mode - press Ctrl+C to stop")
            print("Note: Monitoring implementation would go here")
            success = True
        else:
            print(f"Unknown command: {args.command}")
            success = False

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        await cli.stop_swarm()
        return 1
    except Exception as e:
        print(f"CLI error: {e}")
        await cli.stop_swarm()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
