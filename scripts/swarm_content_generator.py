#!/usr/bin/env python3
"""
Democratic Swarm Content Generator

This script uses the Pydantic AI Democratic Swarm to collaboratively generate
podcast content, analyze engagement potential, and optimize for different platforms.
The swarm democratically decides on content strategy and quality improvements.

Usage:
    python scripts/swarm_content_generator.py

Requirements:
    - OPENAI_API_KEY environment variable
    - All swarm dependencies installed
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add agents package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent
from agents.diagnostic_system import SwarmDiagnosticSystem


class ContentStrategyAgent(PydanticVideoEditorAgent):
    """Agent specialized in content strategy and audience analysis."""

    def __init__(self, agent_name: str, **kwargs):
        super().__init__(agent_name, **kwargs)

        # Override config for content strategy
        if not hasattr(self, 'config') or self.config is None:
            self.config = self._create_content_config()

    def _create_content_config(self):
        from agents.models.agent_config import AgentConfig

        return AgentConfig(
            name=self.agent_name,
            role="Content Strategy Specialist",
            model="gpt-4o",
            system_prompt="""You are a content strategy specialist for a comedy podcast.
            Your expertise includes audience analysis, content optimization,
            engagement prediction, and platform-specific strategies.

            Always provide data-driven recommendations with engagement metrics.""",
            domain_expertise=[
                "content_strategy",
                "audience_analysis",
                "engagement_optimization",
                "platform_analytics",
                "trend_analysis"
            ],
            tools=[
                {
                    "name": "analyze_content_performance",
                    "description": "Analyze content performance metrics",
                    "inputSchema": {
                        "type": "object",
                        "required": ["content", "platform"],
                        "properties": {
                            "content": {"type": "string"},
                            "platform": {"type": "string", "enum": ["youtube", "tiktok", "twitter", "instagram"]},
                            "target_audience": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "optimize_content_strategy",
                    "description": "Optimize content for better engagement",
                    "inputSchema": {
                        "type": "object",
                        "required": ["content", "current_metrics"],
                        "properties": {
                            "content": {"type": "string"},
                            "current_metrics": {"type": "object"},
                            "platform": {"type": "string"}
                        }
                    }
                }
            ],
            max_concurrent_tasks=3,
            voting_enabled=True,
            confidence_thresholds={
                "voting": 0.5,
                "communication": 0.6,
                "execution": 0.7
            }
        )

    async def _execute_tool_core(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        if tool_name == "analyze_content_performance":
            return await self._analyze_content_performance(parameters)
        elif tool_name == "optimize_content_strategy":
            return await self._optimize_content_strategy(parameters)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def _analyze_content_performance(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        content = parameters["content"]
        platform = parameters.get("platform", "youtube")
        target_audience = parameters.get("target_audience", "general")

        analysis = {
            "engagement_potential": self._calculate_engagement_potential(content, platform),
            "virality_score": self._assess_virality(content, platform),
            "audience_fit": self._analyze_audience_fit(content, target_audience),
            "platform_optimization": self._check_platform_optimization(content, platform),
            "content_quality_score": self._assess_content_quality(content),
            "recommendations": self._generate_content_recommendations(content, platform)
        }

        return analysis

    async def _optimize_content_strategy(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        content = parameters["content"]
        current_metrics = parameters.get("current_metrics", {})
        platform = parameters.get("platform", "youtube")

        optimization = {
            "current_performance": current_metrics,
            "optimization_opportunities": self._identify_optimization_opportunities(content, current_metrics, platform),
            "platform_specific_tweaks": self._generate_platform_tweaks(content, platform),
            "predicted_improvement": self._predict_improvement(content, current_metrics),
            "implementation_priority": "high"
        }

        return optimization

    def _calculate_engagement_potential(self, content: str, platform: str) -> Dict[str, Any]:
        score = 0.5

        # Platform-specific engagement factors
        if platform == "tiktok":
            if len(content) < 100:
                score += 0.3  # Short form content
            if any(word in content.lower() for word in ["challenge", "dance", "trend"]):
                score += 0.2
        elif platform == "youtube":
            if len(content) > 200:
                score += 0.2  # Detailed content
            if ":" in content or any(word in content.lower() for word in ["how", "why", "what"]):
                score += 0.3

        return {
            "score": min(1.0, score),
            "level": "high" if score > 0.7 else "medium" if score > 0.4 else "low"
        }

    def _assess_virality(self, content: str, platform: str) -> Dict[str, Any]:
        viral_score = 0.3

        # Viral content indicators
        if any(word in content.lower() for word in ["shocking", "unbelievable", "crazy", "insane"]):
            viral_score += 0.2
        if "?" in content or "!" in content:
            viral_score += 0.1
        if platform == "tiktok" and len(content) < 50:
            viral_score += 0.3

        return {
            "score": min(1.0, viral_score),
            "potential": "high" if viral_score > 0.7 else "medium" if viral_score > 0.4 else "low"
        }

    def _analyze_audience_fit(self, content: str, audience: str) -> Dict[str, Any]:
        fit_score = 0.6

        if audience == "comedy_fans":
            if any(word in content.lower() for word in ["joke", "funny", "laugh", "hilarious"]):
                fit_score += 0.2
        elif audience == "tech_savvy":
            if any(word in content.lower() for word in ["ai", "tech", "code", "software"]):
                fit_score += 0.2

        return {
            "score": min(1.0, fit_score),
            "fit_level": "excellent" if fit_score > 0.8 else "good" if fit_score > 0.6 else "needs_work"
        }

    def _check_platform_optimization(self, content: str, platform: str) -> Dict[str, Any]:
        optimizations = []

        if platform == "tiktok":
            if len(content) > 80:
                optimizations.append("Consider shortening text for TikTok")
            if not any(char in content for char in ["?", "!", "🔥", "😂"]):
                optimizations.append("Add emojis and engagement hooks")
        elif platform == "youtube":
            if len(content) < 150:
                optimizations.append("Add more detail for YouTube audience")
            if not any(word in content.lower() for word in ["subscribe", "like", "comment"]):
                optimizations.append("Include call-to-action phrases")

        return {
            "optimizations_needed": len(optimizations) > 0,
            "suggestions": optimizations,
            "optimization_score": max(0, 1.0 - (len(optimizations) * 0.2))
        }

    def _assess_content_quality(self, content: str) -> Dict[str, Any]:
        quality_score = 0.5

        if len(content) > 50:
            quality_score += 0.2
        if any(char in content for char in [".", "!", "?"]):
            quality_score += 0.1
        if any(word in content.lower() for word in ["comedy", "podcast", "funny"]):
            quality_score += 0.2

        return {
            "score": min(1.0, quality_score),
            "grade": "A" if quality_score > 0.8 else "B" if quality_score > 0.6 else "C" if quality_score > 0.4 else "D"
        }

    def _generate_content_recommendations(self, content: str, platform: str) -> List[str]:
        recommendations = []

        if len(content) < 30:
            recommendations.append("Consider adding more descriptive content")
        if platform == "tiktok" and len(content) > 100:
            recommendations.append("TikTok content should be concise and punchy")
        if not any(word in content.lower() for word in ["comedy", "podcast", "funny"]):
            recommendations.append("Highlight the comedy/podcast aspect for better audience targeting")

        return recommendations or ["Content appears well-optimized for the platform"]

    def _identify_optimization_opportunities(self, content: str, metrics: Dict[str, Any], platform: str) -> List[Dict[str, Any]]:
        opportunities = []

        engagement_rate = metrics.get("engagement_rate", 0.05)

        if engagement_rate < 0.03:
            opportunities.append({
                "type": "hook_improvement",
                "description": "Strengthen the opening hook to capture attention",
                "impact": "high",
                "effort": "medium"
            })

        if platform == "youtube" and len(content) < 200:
            opportunities.append({
                "type": "content_expansion",
                "description": "Add more detailed description for YouTube SEO",
                "impact": "medium",
                "effort": "low"
            })

        return opportunities

    def _generate_platform_tweaks(self, content: str, platform: str) -> List[str]:
        if platform == "tiktok":
            return [
                "Use trending hashtags",
                "Include popular sounds or challenges",
                "Keep text overlay concise and impactful"
            ]
        elif platform == "youtube":
            return [
                "Include timestamps in description",
                "Add relevant tags and keywords",
                "Include calls-to-action in description"
            ]
        else:
            return ["Optimize for platform-specific best practices"]

    def _predict_improvement(self, content: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        base_engagement = current_metrics.get("engagement_rate", 0.05)
        predicted_improvement = base_engagement * 0.3  # 30% improvement

        return {
            "engagement_increase": predicted_improvement,
            "confidence": 0.75,
            "timeframe": "2-4 weeks with consistent optimization"
        }


async def run_content_generation_demo():
    """Run the democratic content generation demo."""
    print("Democratic Swarm Content Generator")
    print("=" * 50)

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable required")
        return 1

    try:
        # Sample content ideas for the podcast
        content_ideas = [
            "Top 10 Comedy Podcast Moments That Made Us Cry Laughing",
            "AI Takes Over Comedy: Can Machines Be Funny?",
            "Behind the Scenes: How We Create Our Podcast Episodes",
            "Comedy Gold: Viral Moments That Changed Social Media"
        ]

        # Create swarm
        swarm = PydanticAISwarmOrchestrator("ContentGenerationSwarm")

        # Create content strategy agents
        agents = []
        for i in range(3):
            agent = ContentStrategyAgent(f"content_agent_{i+1}")
            agents.append(agent)
            await swarm.register_agent(agent)

        print(f"Created swarm with {len(agents)} content strategy agents")

        # Start swarm
        await swarm.start_swarm()

        # Initialize diagnostics
        diagnostics = SwarmDiagnosticSystem(swarm)
        await diagnostics.start_monitoring()

        print("Swarm activated - analyzing content democratically...")

        # Analyze each content idea democratically
        content_analyses = []

        for i, content in enumerate(content_ideas, 1):
            print(f"\nAnalyzing Content Idea {i}: {content[:60]}...")

            # Have all agents analyze the content for different platforms
            platforms = ["youtube", "tiktok", "twitter", "instagram"]
            platform_analyses = {}

            for platform in platforms:
                # Each agent analyzes for this platform
                analysis_tasks = []
                for agent in agents:
                    task = swarm.execute_task(
                        f"Analyze content for {platform} platform",
                        {
                            "domain": "content_strategy",
                            "content": content,
                            "platform": platform,
                            "target_audience": "comedy_fans"
                        }
                    )
                    analysis_tasks.append(task)

                # Collect analyses
                analysis_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
                successful_analyses = [r for r in analysis_results if not isinstance(r, Exception) and r.success]

                if successful_analyses:
                    # Calculate consensus metrics
                    avg_engagement = sum(r.data.get("engagement_potential", {}).get("score", 0.5)
                                       for r in successful_analyses) / len(successful_analyses)
                    avg_virality = sum(r.data.get("virality_score", {}).get("score", 0.3)
                                     for r in successful_analyses) / len(successful_analyses)

                    platform_analyses[platform] = {
                        "analyses": successful_analyses,
                        "consensus_engagement": avg_engagement,
                        "consensus_virality": avg_virality
                    }

                    print(".2f"                    print(".2f"
            # Now have agents vote on the best platform for this content
            voting_tasks = []
            for agent in agents:
                vote_task = swarm.execute_task(
                    f"Vote on best platform for content: {content[:50]}...",
                    {
                        "domain": "content_strategy",
                        "content": content,
                        "platform_analyses": platform_analyses,
                        "voting_context": {"content_type": "podcast_promo", "goal": "maximum_engagement"}
                    }
                )
                voting_tasks.append(vote_task)

            # Collect platform votes
            vote_results = await asyncio.gather(*voting_tasks, return_exceptions=True)
            successful_votes = [r for r in vote_results if not isinstance(r, Exception) and r.success]

            if successful_votes:
                # Count votes by platform
                platform_votes = {}
                for vote in successful_votes:
                    platform = vote.data.get("recommended_platform", "unknown")
                    platform_votes[platform] = platform_votes.get(platform, 0) + 1

                # Find winning platform
                winning_platform = max(platform_votes, key=platform_votes.get)
                confidence = platform_votes[winning_platform] / len(agents)

                content_analyses.append({
                    "content": content,
                    "platform_analyses": platform_analyses,
                    "platform_votes": successful_votes,
                    "recommended_platform": winning_platform,
                    "confidence": confidence,
                    "vote_distribution": platform_votes
                })

                print(f"Democratic Recommendation: {winning_platform.upper()} (confidence: {confidence:.2f})")

        # Generate final content strategy recommendations
        strategy_recommendations = generate_content_strategy(content_analyses)

        # Display results
        display_content_results(strategy_recommendations, content_analyses)

        # Show swarm performance
        final_health = await swarm.analyze_swarm_health()
        print(".2f")
        # Cleanup
        await diagnostics.stop_monitoring()
        await swarm.stop_swarm()

        print("Democratic content generation complete!")
        return 0

    except Exception as e:
        print(f"Content generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def generate_content_strategy(analyses: List[Dict]) -> List[Dict]:
    """Generate final content strategy based on swarm consensus."""
    strategy = []

    for analysis in analyses:
        content = analysis["content"]
        recommended_platform = analysis["recommended_platform"]
        confidence = analysis["confidence"]

        # Get platform-specific analysis
        platform_data = analysis["platform_analyses"].get(recommended_platform, {})
        engagement = platform_data.get("consensus_engagement", 0.5)
        virality = platform_data.get("consensus_virality", 0.3)

        # Calculate overall content score
        content_score = (engagement * 0.5) + (virality * 0.3) + (confidence * 0.2)

        strategy_item = {
            "content": content,
            "recommended_platform": recommended_platform,
            "content_score": content_score,
            "engagement_potential": engagement,
            "virality_potential": virality,
            "confidence": confidence,
            "action": "produce" if content_score > 0.7 else "consider" if content_score > 0.5 else "defer",
            "priority": "high" if content_score > 0.8 else "medium" if content_score > 0.6 else "low"
        }

        strategy.append(strategy_item)

    # Sort by content score
    strategy.sort(key=lambda x: x["content_score"], reverse=True)

    return strategy


def display_content_results(strategy: List[Dict], analyses: List[Dict]):
    """Display the content generation results."""
    print("\nCONTENT GENERATION RESULTS")
    print("=" * 50)

    print("Top Content Recommendations:")
    print("-" * 30)

    for i, item in enumerate(strategy[:4], 1):  # Show top 4
        action_icon = {"produce": "[PRODUCE]", "consider": "[CONSIDER]", "defer": "[DEFER]"}.get(item["action"], "[UNKNOWN]")
        platform = item["recommended_platform"].upper()

        print(f"\n{i}. {action_icon} {item['content']}")
        print(f"   Platform: {platform} (confidence: {item['confidence']:.2f})")
        print(".2f"        print(".2f"        print(f"   Priority: {item['priority'].upper()}")

    print("
Strategy Summary:"    print("-" * 20)
    print(f"   Content Ideas Analyzed: {len(analyses)}")
    print(f"   High Priority Content: {sum(1 for s in strategy if s['priority'] == 'high')}")
    print(f"   Recommended for Production: {sum(1 for s in strategy if s['action'] == 'produce')}")

    # Platform distribution
    platform_distribution = {}
    for item in strategy:
        platform = item["recommended_platform"]
        platform_distribution[platform] = platform_distribution.get(platform, 0) + 1

    print("
Platform Distribution:"    for platform, count in platform_distribution.items():
        percentage = (count / len(strategy)) * 100
        print(".1f"
    print("
Content strategy democratically determined!")


async def main():
    """Main entry point."""
    return await run_content_generation_demo()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
