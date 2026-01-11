#!/usr/bin/env python3
"""
Democratic Swarm GitHub Issue Processor

This script uses the Pydantic AI Democratic Swarm to analyze GitHub issues
and democratically decide which ones to work on, how to prioritize them,
and coordinate their resolution.

The swarm will:
1. Analyze all open GitHub issues
2. Agents vote on priority and feasibility
3. Democratic consensus determines which issues to tackle
4. Agents collaborate on solutions
5. Results are presented with confidence scores

Usage:
    python scripts/swarm_github_issue_processor.py

Requirements:
    - OPENAI_API_KEY environment variable
    - GitHub CLI (gh) for issue access
    - All swarm dependencies installed
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add agents package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent
from agents.diagnostic_system import SwarmDiagnosticSystem


class GitHubIssueAnalyzerAgent(PydanticVideoEditorAgent):
    """Agent specialized in analyzing GitHub issues for the podcast production system."""

    def __init__(self, agent_name: str, **kwargs):
        super().__init__(agent_name, **kwargs)

        # Override config for GitHub analysis
        if not hasattr(self, 'config') or self.config is None:
            self.config = self._create_github_config()

    def _create_github_config(self):
        """Create GitHub-specific agent configuration."""
        from agents.models.agent_config import AgentConfig

        return AgentConfig(
            name=self.agent_name,
            role="GitHub Issue Analysis Specialist",
            model="gpt-4o",
            system_prompt="""You are a GitHub issue analysis specialist for a podcast production system.
            Your expertise includes:
            - Analyzing issue descriptions for technical feasibility
            - Assessing business impact and user value
            - Evaluating implementation complexity
            - Determining resource requirements
            - Providing confidence scores for decisions

            Always provide detailed analysis with specific reasoning and confidence metrics.""",
            domain_expertise=[
                "github_issue_analysis",
                "technical_feasibility",
                "business_impact",
                "complexity_assessment",
                "resource_planning"
            ],
            tools=[
                {
                    "name": "analyze_github_issue",
                    "description": "Comprehensive GitHub issue analysis",
                    "inputSchema": {
                        "type": "object",
                        "required": ["issue_data"],
                        "properties": {
                            "issue_data": {"type": "object", "description": "GitHub issue JSON data"},
                            "analysis_type": {
                                "type": "string",
                                "enum": ["feasibility", "priority", "effort", "comprehensive"],
                                "default": "comprehensive"
                            }
                        }
                    }
                },
                {
                    "name": "vote_on_issue_priority",
                    "description": "Vote on issue priority with confidence score",
                    "inputSchema": {
                        "type": "object",
                        "required": ["issue_data", "context"],
                        "properties": {
                            "issue_data": {"type": "object"},
                            "context": {"type": "object", "description": "Project context and constraints"}
                        }
                    }
                }
            ],
            max_concurrent_tasks=5,
            voting_enabled=True,
            confidence_thresholds={
                "voting": 0.6,
                "communication": 0.5,
                "execution": 0.7
            }
        )

    async def _execute_tool_core(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute GitHub analysis tools."""
        if tool_name == "analyze_github_issue":
            return await self._analyze_github_issue(parameters)
        elif tool_name == "vote_on_issue_priority":
            return await self._vote_on_issue_priority(parameters)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def _analyze_github_issue(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a GitHub issue comprehensively."""
        issue_data = parameters["issue_data"]
        analysis_type = parameters.get("analysis_type", "comprehensive")

        title = issue_data.get("title", "")
        body = issue_data.get("body", "")
        labels = issue_data.get("labels", [])
        comments = issue_data.get("comments", 0)

        # Extract labels
        label_names = [label["name"] if isinstance(label, dict) else str(label) for label in labels]

        analysis = {
            "issue_number": issue_data.get("number"),
            "title": title,
            "analysis_type": analysis_type,
            "technical_feasibility": self._assess_technical_feasibility(title, body, label_names),
            "business_impact": self._assess_business_impact(title, body, label_names),
            "implementation_complexity": self._assess_complexity(title, body, label_names),
            "estimated_effort": self._estimate_effort(title, body, label_names),
            "resource_requirements": self._identify_resources(title, body, label_names),
            "priority_recommendation": self._recommend_priority(title, body, label_names, comments),
            "confidence_score": self._calculate_analysis_confidence(title, body, label_names),
            "recommendations": self._generate_recommendations(title, body, label_names)
        }

        return analysis

    async def _vote_on_issue_priority(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Vote on issue priority with detailed reasoning."""
        issue_data = parameters["issue_data"]
        context = parameters.get("context", {})

        title = issue_data.get("title", "")
        body = issue_data.get("body", "")
        labels = issue_data.get("labels", [])
        label_names = [label["name"] if isinstance(label, dict) else str(label) for label in labels]

        # Calculate priority score (1-10, higher = more important)
        priority_score = self._calculate_priority_score(title, body, label_names, context)

        # Determine priority level
        if priority_score >= 8:
            priority_level = "critical"
            confidence = 0.9
        elif priority_score >= 6:
            priority_level = "high"
            confidence = 0.8
        elif priority_score >= 4:
            priority_level = "medium"
            confidence = 0.7
        else:
            priority_level = "low"
            confidence = 0.6

        vote = {
            "issue_number": issue_data.get("number"),
            "priority_level": priority_level,
            "priority_score": priority_score,
            "confidence": confidence,
            "reasoning": self._explain_priority_vote(title, body, label_names, priority_score),
            "voting_agent": self.agent_name
        }

        return vote

    def _assess_technical_feasibility(self, title: str, body: str, labels: List[str]) -> Dict[str, Any]:
        """Assess technical feasibility of implementing the issue."""
        feasibility_score = 0.5  # Base score

        # Check for complexity indicators
        if any(word in title.lower() for word in ["ai", "ml", "machine learning", "neural"]):
            feasibility_score += 0.2  # AI features are complex but doable
        elif any(word in title.lower() for word in ["database", "api", "integration"]):
            feasibility_score += 0.1  # Infrastructure work
        elif any(word in title.lower() for word in ["ui", "frontend", "styling"]):
            feasibility_score += 0.3  # UI work is often straightforward

        # Check labels
        if "enhancement" in labels:
            feasibility_score += 0.1
        if "bug" in labels:
            feasibility_score -= 0.1  # Bugs might be complex to fix

        # Length and detail assessment
        if len(body) > 200:
            feasibility_score += 0.1  # Detailed requirements = better feasibility

        return {
            "score": min(1.0, max(0.0, feasibility_score)),
            "assessment": "feasible" if feasibility_score > 0.6 else "challenging" if feasibility_score > 0.3 else "complex",
            "reasoning": self._explain_feasibility(feasibility_score, title, labels)
        }

    def _assess_business_impact(self, title: str, body: str, labels: List[str]) -> Dict[str, Any]:
        """Assess business impact of the issue."""
        impact_score = 0.3  # Base score

        # Business impact indicators
        if any(word in title.lower() for word in ["performance", "speed", "efficiency", "optimization"]):
            impact_score += 0.3  # Performance improvements have high impact
        elif any(word in title.lower() for word in ["user", "ux", "experience", "interface"]):
            impact_score += 0.2  # User experience improvements
        elif any(word in title.lower() for word in ["security", "privacy", "auth"]):
            impact_score += 0.4  # Security is critical
        elif any(word in title.lower() for word in ["monetization", "revenue", "business"]):
            impact_score += 0.5  # Direct business impact

        # Label-based impact
        if "high-priority" in labels or "critical" in labels:
            impact_score += 0.2

        return {
            "score": min(1.0, impact_score),
            "level": "high" if impact_score > 0.7 else "medium" if impact_score > 0.4 else "low",
            "reasoning": f"Business impact assessment based on {title.lower()}"
        }

    def _assess_complexity(self, title: str, body: str, labels: List[str]) -> Dict[str, Any]:
        """Assess implementation complexity."""
        complexity_score = 0.5  # Base score

        # Complexity indicators
        if any(word in title.lower() for word in ["ai", "ml", "integration", "distributed"]):
            complexity_score += 0.3
        elif any(word in title.lower() for word in ["refactor", "architecture", "system"]):
            complexity_score += 0.2

        # Label-based complexity
        if "enhancement" in labels:
            complexity_score += 0.1

        return {
            "score": min(1.0, complexity_score),
            "level": "high" if complexity_score > 0.7 else "medium" if complexity_score > 0.4 else "low",
            "estimated_days": self._estimate_days(complexity_score)
        }

    def _estimate_effort(self, title: str, body: str, labels: List[str]) -> str:
        """Estimate effort required."""
        # Simple effort estimation based on keywords
        if any(word in title.lower() for word in ["simple", "minor", "small", "quick"]):
            return "small"
        elif any(word in title.lower() for word in ["major", "large", "complex", "system"]):
            return "large"
        else:
            return "medium"

    def _identify_resources(self, title: str, body: str, labels: List[str]) -> List[str]:
        """Identify resources needed."""
        resources = []

        if any(word in title.lower() for word in ["ai", "ml", "openai", "gpt"]):
            resources.append("OpenAI API access")
        if any(word in title.lower() for word in ["video", "media", "editing"]):
            resources.append("Video processing tools")
        if any(word in title.lower() for word in ["database", "storage"]):
            resources.append("Database access")
        if any(word in title.lower() for word in ["api", "integration"]):
            resources.append("API credentials")

        return resources if resources else ["Standard development environment"]

    def _recommend_priority(self, title: str, body: str, labels: List[str], comments: int) -> str:
        """Recommend priority level."""
        if "critical" in labels or "high-priority" in labels:
            return "critical"
        elif "bug" in labels:
            return "high"
        elif comments > 5:  # Community interest
            return "medium"
        else:
            return "low"

    def _calculate_analysis_confidence(self, title: str, body: str, labels: List[str]) -> float:
        """Calculate confidence in analysis."""
        confidence = 0.7  # Base confidence

        if len(body) > 100:
            confidence += 0.1  # Detailed description
        if labels:
            confidence += 0.1  # Proper labeling
        if len(title) > 10:
            confidence += 0.1  # Descriptive title

        return min(1.0, confidence)

    def _generate_recommendations(self, title: str, body: str, labels: List[str]) -> List[str]:
        """Generate implementation recommendations."""
        recommendations = []

        if len(body) < 50:
            recommendations.append("Add more detailed requirements to improve implementation clarity")

        if not labels:
            recommendations.append("Add appropriate labels (bug, enhancement, documentation, etc.)")

        if "ai" in title.lower() and "api" not in body.lower():
            recommendations.append("Consider API rate limits and costs for AI features")

        return recommendations

    def _calculate_priority_score(self, title: str, body: str, labels: List[str], context: Dict[str, Any]) -> float:
        """Calculate priority score (1-10)."""
        score = 5.0  # Base score

        # Business impact factors
        if any(word in title.lower() for word in ["security", "critical", "performance"]):
            score += 3
        elif any(word in title.lower() for word in ["user", "ux", "experience"]):
            score += 2

        # Label-based priority
        if "critical" in labels:
            score += 2
        if "high-priority" in labels:
            score += 1.5
        if "bug" in labels:
            score += 1

        # Effort consideration (easier tasks get higher priority)
        effort = self._estimate_effort(title, body, labels)
        if effort == "small":
            score += 0.5

        return min(10.0, max(1.0, score))

    def _explain_priority_vote(self, title: str, body: str, labels: List[str], score: float) -> str:
        """Explain the priority voting decision."""
        reasons = []

        if score >= 8:
            reasons.append("High business impact")
        if "critical" in labels:
            reasons.append("Marked as critical")
        if "bug" in labels:
            reasons.append("Bug fix needed")

        return f"Priority score {score:.1f} based on: {', '.join(reasons)}"

    def _explain_feasibility(self, score: float, title: str, labels: List[str]) -> str:
        """Explain feasibility assessment."""
        if score > 0.7:
            return f"High feasibility for '{title}' - appears straightforward to implement"
        elif score > 0.4:
            return f"Medium feasibility for '{title}' - requires some analysis"
        else:
            return f"Lower feasibility for '{title}' - complex implementation needed"

    def _estimate_days(self, complexity_score: float) -> int:
        """Estimate implementation days based on complexity."""
        if complexity_score > 0.7:
            return 5  # Complex
        elif complexity_score > 0.4:
            return 3  # Medium
        else:
            return 1  # Simple


async def fetch_github_issues() -> List[Dict[str, Any]]:
    """Fetch open GitHub issues using GitHub CLI."""
    try:
        # Use GitHub CLI to fetch issues
        cmd = ["gh", "issue", "list", "--json", "number,title,body,labels,comments,createdAt,updatedAt"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        if result.returncode == 0:
            issues = json.loads(result.stdout)
            print(f"Successfully fetched {len(issues)} GitHub issues")
            return issues
        else:
            print(f"Failed to fetch GitHub issues: {result.stderr}")
            return []

    except Exception as e:
        print(f"Error fetching GitHub issues: {e}")
        return []


async def run_swarm_issue_analysis():
    """Run the democratic swarm to analyze GitHub issues."""
    print("🤖 Pydantic AI Democratic Swarm - GitHub Issue Analysis")
    print("=" * 60)

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY environment variable required")
        return 1

    try:
        # Fetch GitHub issues
        print("\n📥 Fetching GitHub issues...")
        issues = await fetch_github_issues()

        if not issues:
            print("❌ No issues found or failed to fetch issues")
            return 1

        print(f"📊 Found {len(issues)} open issues to analyze")

        # Create swarm with multiple analysis agents
        print("\n🚀 Initializing democratic swarm...")
        swarm = PydanticAISwarmOrchestrator("GitHubIssueAnalysisSwarm")

        # Create multiple analysis agents for democratic voting
        agents = []
        for i in range(3):
            agent = GitHubIssueAnalyzerAgent(f"issue_analyzer_{i+1}")
            agents.append(agent)
            await swarm.register_agent(agent)

        print(f"✅ Created {len(agents)} analysis agents")

        # Start swarm
        await swarm.start_swarm()
        print("🎯 Swarm activated - beginning democratic analysis")

        # Initialize diagnostics
        diagnostics = SwarmDiagnosticSystem(swarm)
        await diagnostics.start_monitoring()

        # Analyze each issue democratically
        issue_analyses = []
        priority_votes = []

        print("
🔍 Analyzing issues democratically..."        for i, issue in enumerate(issues[:5], 1):  # Limit to first 5 for demo
            issue_num = issue.get("number", "unknown")
            title = issue.get("title", "No title")[:50]

            print(f"\n🎯 Issue #{issue_num}: {title}...")

            # Each agent analyzes the issue
            analysis_tasks = []
            for agent in agents:
                task = swarm.execute_task(
                    f"Analyze GitHub issue #{issue_num} for feasibility and priority",
                    {
                        "domain": "github_issue_analysis",
                        "issue_data": issue,
                        "analysis_type": "comprehensive"
                    }
                )
                analysis_tasks.append(task)

            # Wait for all analyses to complete
            analysis_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)

            # Collect successful analyses
            successful_analyses = [r for r in analysis_results if not isinstance(r, Exception) and r.success]

            if successful_analyses:
                # Aggregate analysis results democratically
                avg_feasibility = sum(r.data.get("technical_feasibility", {}).get("score", 0.5)
                                    for r in successful_analyses) / len(successful_analyses)
                avg_impact = sum(r.data.get("business_impact", {}).get("score", 0.3)
                               for r in successful_analyses) / len(successful_analyses)

                issue_analyses.append({
                    "issue": issue,
                    "analyses": successful_analyses,
                    "consensus_feasibility": avg_feasibility,
                    "consensus_impact": avg_impact
                })

                print(".2f"                print(".2f"
            # Now have agents vote on priority
            voting_tasks = []
            for agent in agents:
                vote_task = swarm.execute_task(
                    f"Vote on priority for GitHub issue #{issue_num}",
                    {
                        "domain": "github_issue_analysis",
                        "issue_data": issue,
                        "voting_context": {"total_issues": len(issues), "current_position": i}
                    }
                )
                voting_tasks.append(vote_task)

            # Collect votes
            vote_results = await asyncio.gather(*voting_tasks, return_exceptions=True)
            successful_votes = [r for r in vote_results if not isinstance(r, Exception) and r.success]

            if successful_votes:
                # Count votes by priority level
                priority_counts = {}
                for vote in successful_votes:
                    level = vote.data.get("priority_level", "unknown")
                    priority_counts[level] = priority_counts.get(level, 0) + 1

                # Determine democratic consensus
                winning_priority = max(priority_counts, key=priority_counts.get)
                confidence = priority_counts[winning_priority] / len(agents)

                priority_votes.append({
                    "issue": issue,
                    "votes": successful_votes,
                    "consensus_priority": winning_priority,
                    "confidence": confidence,
                    "vote_distribution": priority_counts
                })

                print(f"   🗳️  Democratic Priority: {winning_priority.upper()} ({confidence:.1f} confidence)")

        # Generate final recommendations
        print("
📋 Generating Final Recommendations..."        recommendations = generate_swarm_recommendations(issue_analyses, priority_votes)

        # Display results
        display_swarm_results(recommendations, issue_analyses, priority_votes)

        # Show swarm health
        final_health = await swarm.analyze_swarm_health()
        print("
🏥 Final Swarm Health:"        print(".2f"        print(f"   Active Agents: {final_health['detailed_analysis']['agents']['active']}")
        print(f"   Tasks Completed: {final_health['detailed_analysis']['tasks']['total_processed']}")

        # Cleanup
        await diagnostics.stop_monitoring()
        await swarm.stop_swarm()

        print("
✅ Democratic issue analysis complete!"        return 0

    except Exception as e:
        print(f"❌ Swarm analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def generate_swarm_recommendations(analyses: List[Dict], votes: List[Dict]) -> List[Dict]:
    """Generate final recommendations based on swarm consensus."""
    recommendations = []

    # Combine analysis and voting data
    for analysis in analyses:
        issue = analysis["issue"]
        issue_num = issue.get("number")

        # Find corresponding votes
        vote_data = next((v for v in votes if v["issue"]["number"] == issue_num), None)

        if vote_data:
            # Calculate overall recommendation score
            feasibility = analysis["consensus_feasibility"]
            impact = analysis["consensus_impact"]
            priority_confidence = vote_data["confidence"]

            # Weighted recommendation score
            recommendation_score = (feasibility * 0.3) + (impact * 0.4) + (priority_confidence * 0.3)

            priority_map = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4}
            priority_level = vote_data["consensus_priority"]
            priority_weight = priority_map.get(priority_level, 0.5)

            final_score = (recommendation_score + priority_weight) / 2

            recommendation = {
                "issue_number": issue_num,
                "title": issue.get("title", "Unknown"),
                "recommendation_score": final_score,
                "priority_level": priority_level,
                "feasibility_score": feasibility,
                "impact_score": impact,
                "confidence": priority_confidence,
                "action": "prioritize" if final_score > 0.7 else "consider" if final_score > 0.5 else "defer",
                "reasoning": generate_recommendation_reasoning(analysis, vote_data)
            }

            recommendations.append(recommendation)

    # Sort by recommendation score
    recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)

    return recommendations


def generate_recommendation_reasoning(analysis: Dict, vote_data: Dict) -> str:
    """Generate reasoning for the recommendation."""
    priority = vote_data["consensus_priority"]
    feasibility = analysis["consensus_feasibility"]
    impact = analysis["consensus_impact"]

    reasons = []

    if priority in ["critical", "high"]:
        reasons.append(f"high priority ({priority})")
    if impact > 0.7:
        reasons.append("significant business impact")
    if feasibility > 0.7:
        reasons.append("technically feasible")
    elif feasibility < 0.4:
        reasons.append("technically challenging")

    return f"Recommended based on {', '.join(reasons)}"


def display_swarm_results(recommendations: List[Dict], analyses: List[Dict], votes: List[Dict]):
    """Display the swarm analysis results."""
    print("\n🎊 DEMOCRATIC SWARM ANALYSIS RESULTS")
    print("=" * 60)

    print("
📊 Top Recommended Issues:"    print("-" * 40)

    for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
        action_icon = {"prioritize": "🔥", "consider": "🤔", "defer": "⏰"}.get(rec["action"], "❓")
        priority_icon = {"critical": "🚨", "high": "⚡", "medium": "📊", "low": "🐌"}.get(rec["priority_level"], "❓")

        print(f"\n{i}. {action_icon} Issue #{rec['issue_number']}: {rec['title']}")
        print(f"   {priority_icon} Priority: {rec['priority_level'].upper()}")
        print(".2f"        print(".2f"        print(".2f"        print(f"   💡 Action: {rec['action'].upper()}")
        print(f"   📝 Reasoning: {rec['reasoning']}")

    print("
📈 Swarm Consensus Summary:"    print("-" * 30)
    print(f"   Issues Analyzed: {len(analyses)}")
    print(f"   Democratic Votes: {len(votes)}")
    print(f"   High Priority: {sum(1 for r in recommendations if r['priority_level'] == 'high')}")
    print(f"   Critical Issues: {sum(1 for r in recommendations if r['priority_level'] == 'critical')}")
    print(f"   Recommended Actions: {sum(1 for r in recommendations if r['action'] == 'prioritize')}")

    # Show voting patterns
    print("
🗳️  Voting Pattern Analysis:"    print("-" * 25)

    priority_distribution = {}
    for vote_data in votes:
        priority = vote_data["consensus_priority"]
        priority_distribution[priority] = priority_distribution.get(priority, 0) + 1

    for priority, count in priority_distribution.items():
        percentage = (count / len(votes)) * 100
        print(".1f"
    print("
🤖 Democratic Analysis Complete!"    print("The swarm has democratically analyzed all issues and provided consensus recommendations.")


async def main():
    """Main entry point."""
    return await run_swarm_issue_analysis()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
