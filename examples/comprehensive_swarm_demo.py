#!/usr/bin/env python3
"""
Comprehensive Pydantic AI Democratic Swarm Demo

This script demonstrates all major features of the Pydantic AI Democratic Agent Swarm:
- Agent creation and registration
- Democratic task assignment and voting
- Tool execution and caching
- Health monitoring and diagnostics
- Performance analytics and reporting
- Error recovery and fault tolerance

Usage:
    python examples/comprehensive_swarm_demo.py

Requirements:
    - OpenAI API key in environment
    - All dependencies installed
"""

import asyncio
import logging
import time
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the swarm system
from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent
from agents.diagnostic_system import SwarmDiagnosticSystem
from agents.tools import tool_factory, VideoAnalysisTool, AutoCutTool


class DemoRunner:
    """Comprehensive demo runner for the Pydantic AI Swarm system."""

    def __init__(self):
        self.swarm: PydanticAISwarmOrchestrator = None
        self.diagnostics: SwarmDiagnosticSystem = None
        self.start_time = time.time()

    async def setup_swarm(self) -> None:
        """Set up the swarm with multiple agents and tools."""
        print("🚀 Setting up Pydantic AI Democratic Swarm...")

        # Create swarm orchestrator
        self.swarm = PydanticAISwarmOrchestrator(
            swarm_name="ComprehensiveDemoSwarm",
            enable_diagnostics=True,
            enable_monitoring=True,
            enable_benchmarking=True
        )

        # Create specialized agents
        agents = [
            PydanticVideoEditorAgent("video_editor_1"),
            PydanticVideoEditorAgent("video_editor_2"),
            PydanticVideoEditorAgent("content_analyst"),
        ]

        print(f"📝 Created {len(agents)} specialized agents")

        # Register agents with the swarm
        for agent in agents:
            await self.swarm.register_agent(agent)
            print(f"✅ Registered agent: {agent.agent_name}")

        # Register tools with the factory
        video_tool = VideoAnalysisTool()
        cut_tool = AutoCutTool()

        await tool_factory.register_tool_with_registry(video_tool, "demo")
        await tool_factory.register_tool_with_registry(cut_tool, "demo")

        print("🔧 Registered tools: video_analysis, auto_cut")

        # Initialize diagnostics
        self.diagnostics = SwarmDiagnosticSystem(self.swarm)
        await self.diagnostics.start_monitoring()

        print("📊 Started diagnostic monitoring")

    async def demonstrate_swarm_lifecycle(self) -> None:
        """Demonstrate swarm startup, operation, and shutdown."""
        print("\n🔄 === SWARM LIFECYCLE DEMO ===")

        # Start the swarm
        print("▶️  Starting swarm...")
        await self.swarm.start_swarm()

        # Check initial status
        status = await self.swarm.get_swarm_status()
        print(f"📊 Swarm Status: {status['agents']['active']}/{status['agents']['total']} agents active")

        # Wait a moment for stabilization
        await asyncio.sleep(2)

        # Check health
        health = await self.swarm.analyze_swarm_health()
        print(".2f"
    async def demonstrate_democratic_task_assignment(self) -> None:
        """Demonstrate democratic task assignment and voting."""
        print("\n🗳️  === DEMOCRATIC TASK ASSIGNMENT DEMO ===")

        tasks = [
            {
                "description": "Analyze video for speaker detection and engagement",
                "context": {"domain": "video_editing", "priority": "high"},
                "expected_agent_count": 3
            },
            {
                "description": "Create automatic cuts for social media content",
                "context": {"domain": "video_editing", "priority": "medium"},
                "expected_agent_count": 2
            },
            {
                "description": "Optimize video for TikTok algorithm",
                "context": {"domain": "content_creation", "priority": "low"},
                "expected_agent_count": 1
            }
        ]

        for i, task in enumerate(tasks, 1):
            print(f"\n🎯 Task {i}: {task['description'][:50]}...")

            start_time = time.time()
            result = await self.swarm.execute_task(
                task["description"],
                task["context"]
            )
            execution_time = time.time() - start_time

            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            print(".2f"
            if result.success:
                print(f"   📝 Agent: {result.agent_name}")
                print(f"   📊 Data keys: {list(result.data.keys()) if result.data else 'None'}")

    async def demonstrate_tool_execution(self) -> None:
        """Demonstrate tool execution and caching."""
        print("\n🔧 === TOOL EXECUTION DEMO ===")

        registry = tool_factory.get_registry()

        # Test video analysis tool
        print("🎬 Testing Video Analysis Tool...")
        result1 = await registry.execute_tool(
            "video_analysis",
            {"video_path": "/demo/video.mp4", "analysis_type": "speaker_detection"},
            "demo"
        )
        print(f"   Result: {'✅ Success' if result1.success else '❌ Failed'}")

        # Test caching (same parameters)
        print("🗄️  Testing Tool Caching...")
        start_time = time.time()
        result2 = await registry.execute_tool(
            "video_analysis",
            {"video_path": "/demo/video.mp4", "analysis_type": "speaker_detection"},
            "demo"
        )
        cache_time = time.time() - start_time
        print(".3f"
        # Test auto-cut tool
        print("✂️  Testing Auto Cut Tool...")
        cuts = [
            {"start_time": 0, "end_time": 30, "speaker": "host"},
            {"start_time": 30, "end_time": 60, "speaker": "guest"}
        ]
        result3 = await registry.execute_tool(
            "auto_cut",
            {"video_path": "/demo/video.mp4", "cuts": cuts},
            "demo"
        )
        print(f"   Result: {'✅ Success' if result3.success else '❌ Failed'}")

        # Show registry stats
        stats = registry.get_registry_stats()
        print("
📈 Registry Statistics:"        print(f"   Tools: {stats['total_tools']}")
        print(f"   Executions: {stats['total_calls']}")
        print(f"   Cache entries: {len(stats['cache_entries'])}")

    async def demonstrate_health_monitoring(self) -> None:
        """Demonstrate health monitoring and diagnostics."""
        print("\n🏥 === HEALTH MONITORING DEMO ===")

        # Get comprehensive health analysis
        health = await self.swarm.analyze_swarm_health()

        print("Swarm Health Report:")
        print(".2f"        print(f"   Status: {health['health_status']}")

        # Agent health details
        agent_health = health['detailed_analysis']['agents']
        print(f"   Agents: {agent_health['active']}/{agent_health['total']} active")

        # Task performance
        task_health = health['detailed_analysis']['tasks']
        print(".2f"        print(f"   Average Duration: {task_health['average_duration']:.2f}s")

        # Recommendations
        if health.get('recommendations'):
            print(f"   💡 Recommendations: {len(health['recommendations'])}")
            for rec in health['recommendations'][:2]:  # Show first 2
                print(f"      • {rec['title']}")

        # Run diagnostics scan
        print("
🔍 Running Diagnostic Scan..."        issues = await self.diagnostics.run_diagnostics()
        print(f"   Found {len(issues)} diagnostic issues")

        if issues:
            print("   Sample issues:")
            for issue in issues[:2]:  # Show first 2
                print(f"      • {issue.title} ({issue.severity})")

    async def demonstrate_performance_analytics(self) -> None:
        """Demonstrate performance analytics and reporting."""
        print("\n📊 === PERFORMANCE ANALYTICS DEMO ===")

        # Generate performance report
        report = await self.swarm.generate_performance_report()

        print("Performance Report Summary:")
        print(f"   Report ID: {report['report_id']}")
        print(f"   Duration: {report['time_range']['duration_hours']:.1f} hours")

        # Summary metrics
        metrics = report['summary_metrics']
        print("
📈 Key Metrics:"        print(f"   Tasks Processed: {metrics['total_tasks']}")
        print(".2f"        print(".2f"        print(".2f"        print(f"   Peak Memory: {metrics['peak_memory_mb']:.1f} MB")

        # Benchmarks
        if 'benchmarks' in report:
            benchmarks = report['benchmarks']
            print("
⚡ Performance Benchmarks:"            print(".1f"            print(".2f"
        # Recommendations
        if report.get('recommendations'):
            print("
💡 Recommendations:"            for rec in report['recommendations'][:3]:  # Show first 3
                print(f"      • {rec}")

    async def demonstrate_error_recovery(self) -> None:
        """Demonstrate error recovery and fault tolerance."""
        print("\n🛠️  === ERROR RECOVERY DEMO ===")

        # Test with invalid parameters
        print("Testing tool with invalid parameters...")
        registry = tool_factory.get_registry()

        result = await registry.execute_tool(
            "video_analysis",
            {"invalid_param": "test"},  # Missing required video_path
            "demo"
        )
        print(f"   Expected failure: {'✅ Correctly failed' if not result.success else '❌ Should have failed'}")
        if not result.success:
            print(f"   Error: {result.error[:100]}...")

        # Test swarm with unavailable agent scenario
        print("
Testing swarm fault tolerance..."        # This would normally test agent failure scenarios
        # For demo purposes, we'll show the current status
        status = await self.swarm.get_swarm_status()
        print(f"   Swarm remains operational: {status['is_active']}")
        print(f"   Active agents: {status['agents']['active']}")

        # Show error tracking
        error_count = len(self.swarm.metrics.recent_errors)
        print(f"   Recent errors tracked: {error_count}")

    async def demonstrate_agent_interaction(self) -> None:
        """Demonstrate agent-to-agent interaction and communication."""
        print("\n🤝 === AGENT INTERACTION DEMO ===")

        # Get agent details
        agents = list(self.swarm.agents.values())
        if len(agents) >= 2:
            agent1, agent2 = agents[:2]

            print(f"Testing interaction between {agent1.agent_name} and {agent2.agent_name}")

            # Get individual agent statuses
            status1 = await agent1.get_status_async()
            status2 = await agent2.get_status_async()

            print(f"   {agent1.agent_name} confidence: {status1['confidence']['overall']:.2f}")
            print(f"   {agent2.agent_name} confidence: {status2['confidence']['overall']:.2f}")

            # Show democratic voting capability
            vote1 = await agent1.cast_vote("Test proposal for agent coordination", "general")
            vote2 = await agent2.cast_vote("Test proposal for agent coordination", "general")

            print("   Voting results:")
            print(f"      {agent1.agent_name}: {vote1['decision']} (weight: {vote1['weight']:.2f})")
            print(f"      {agent2.agent_name}: {vote2['decision']} (weight: {vote2['weight']:.2f})")

    async def run_full_demo(self) -> None:
        """Run the complete comprehensive demo."""
        print("🎭 PYDANTIC AI DEMOCRATIC SWARM - COMPREHENSIVE DEMO")
        print("=" * 70)

        try:
            # Setup phase
            await self.setup_swarm()

            # Demonstration phases
            await self.demonstrate_swarm_lifecycle()
            await self.demonstrate_democratic_task_assignment()
            await self.demonstrate_tool_execution()
            await self.demonstrate_health_monitoring()
            await self.demonstrate_performance_analytics()
            await self.demonstrate_error_recovery()
            await self.demonstrate_agent_interaction()

            # Final status
            await self.show_final_status()

        except Exception as e:
            logger.error(f"Demo failed with error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            await self.cleanup()

    async def show_final_status(self) -> None:
        """Show final swarm status and summary."""
        print("\n🎉 === DEMO COMPLETION SUMMARY ===")

        total_time = time.time() - self.start_time

        # Final swarm status
        final_status = await self.swarm.get_swarm_status()
        final_health = await self.swarm.analyze_swarm_health()

        print("📊 Final Swarm Status:")
        print(".1f"        print(f"   Agents: {final_status['agents']['active']}/{final_status['agents']['total']} active")
        print(f"   Tasks Completed: {final_status['tasks']['total_processed']}")
        print(".2f"
        print("
🏥 Final Health:"        print(".2f"        print(f"   Status: {final_health['health_status']}")

        # Performance summary
        metrics = self.swarm.metrics
        print("
⚡ Performance Summary:"        print(f"   Total Tasks: {metrics.total_tasks_processed}")
        print(f"   Success Rate: {metrics.get_success_rate():.2f}")
        print(".2f"        print(f"   Peak Memory: {metrics.peak_memory_usage_mb:.1f} MB")

        print("
✅ Demo completed successfully!"        print("🎯 Demonstrated: Democratic governance, fault tolerance, monitoring, analytics"
    async def cleanup(self) -> None:
        """Clean up resources."""
        print("\n🧹 Cleaning up...")

        if self.diagnostics:
            await self.diagnostics.stop_monitoring()

        if self.swarm and self.swarm.is_active:
            await self.swarm.stop_swarm()

        print("✅ Cleanup complete")


async def main():
    """Main demo entry point."""
    demo = DemoRunner()
    await demo.run_full_demo()


if __name__ == "__main__":
    print("Starting Comprehensive Pydantic AI Swarm Demo...")
    print("Make sure your OPENAI_API_KEY is set in the environment!")
    print("-" * 60)

    asyncio.run(main())
