#!/usr/bin/env python3
"""Run Democratic Agent Swarm on GitHub Issues - Production Task Execution.

This script loads GitHub issues from the .github/issues directory and assigns them
as tasks to the democratic agent swarm, allowing agents to work collaboratively
until all issues are resolved.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from production_swarm_launcher import ProductionSwarmManager, SwarmConfig
from swarm_observability import SwarmObservabilityManager


class GitHubIssueLoader:
    """Load and parse GitHub issues for swarm processing."""

    def __init__(self, issues_dir: str = ".github/issues"):
        """Initialize issue loader.

        Args:
            issues_dir: Directory containing GitHub issue files
        """
        self.issues_dir = Path(issues_dir)
        self.logger = logging.getLogger(__name__)

    def load_all_issues(self) -> List[Dict[str, Any]]:
        """Load all GitHub issues from the directory.

        Returns:
            List of issue dictionaries
        """
        issues = []

        if not self.issues_dir.exists():
            self.logger.error(f"Issues directory not found: {self.issues_dir}")
            return issues

        # Load all markdown files as issues
        for issue_file in self.issues_dir.glob("*.md"):
            if issue_file.name in ["README.md", "SEO_OVERHAUL_COMPLETE.md"]:
                continue  # Skip non-issue files

            try:
                issue = self._parse_issue_file(issue_file)
                if issue:
                    issues.append(issue)
            except Exception as e:
                self.logger.error(f"Failed to parse issue {issue_file}: {e}")

        self.logger.info(f"Loaded {len(issues)} GitHub issues")
        return issues

    def _parse_issue_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a single issue file.

        Args:
            file_path: Path to the issue file

        Returns:
            Parsed issue dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract issue number from filename
        filename = file_path.stem
        issue_number = None

        # Try to extract number from filename (e.g., "001-transcription-agent.md" -> 1)
        if filename.split('-')[0].isdigit():
            issue_number = int(filename.split('-')[0])

        # Extract title from first line (assuming it starts with #)
        lines = content.split('\n')
        title = filename.replace('-', ' ').title()  # Default title from filename

        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                break

        # Extract labels/context from content
        labels = self._extract_labels(content)
        context = self._determine_context(labels, content)

        # Create issue dictionary
        issue = {
            'id': f"github_issue_{issue_number or int(time.time())}",
            'number': issue_number,
            'title': title,
            'description': content[:500] + "..." if len(content) > 500 else content,
            'full_content': content,
            'labels': labels,
            'context': context,
            'type': self._determine_task_type(labels, content),
            'priority': self._determine_priority(labels, content),
            'estimated_complexity': self._estimate_complexity(content),
            'file_path': str(file_path),
            'status': 'open'
        }

        return issue

    def _extract_labels(self, content: str) -> List[str]:
        """Extract labels from issue content."""
        labels = []

        # Look for common labels in content
        label_indicators = {
            'agent': ['agent', 'AI', 'automation'],
            'video': ['video', 'editing', 'media'],
            'audio': ['audio', 'sound', 'music'],
            'social': ['social', 'media', 'posting'],
            'content': ['content', 'distribution', 'publishing'],
            'infrastructure': ['infrastructure', 'deployment', 'CI/CD'],
            'website': ['website', 'frontend', 'UI'],
            'api': ['API', 'integration', 'client'],
            'testing': ['test', 'QA', 'validation'],
            'documentation': ['docs', 'documentation', 'README']
        }

        content_lower = content.lower()

        for label, keywords in label_indicators.items():
            if any(keyword in content_lower for keyword in keywords):
                labels.append(label)

        return labels

    def _determine_context(self, labels: List[str], content: str) -> str:
        """Determine the primary context for the issue."""
        if 'video' in labels:
            return 'video_editing'
        elif 'audio' in labels:
            return 'audio_production'
        elif 'social' in labels:
            return 'social_media'
        elif 'content' in labels:
            return 'content_distribution'
        elif 'agent' in labels:
            return 'agent_development'
        elif 'infrastructure' in labels:
            return 'infrastructure'
        elif 'website' in labels:
            return 'web_development'
        else:
            return 'general'

    def _determine_task_type(self, labels: List[str], content: str) -> str:
        """Determine the task type for the issue."""
        if 'agent' in labels:
            return 'agent_implementation'
        elif 'video' in labels:
            return 'video_processing'
        elif 'audio' in labels:
            return 'audio_processing'
        elif 'social' in labels:
            return 'social_media_management'
        elif 'content' in labels:
            return 'content_distribution'
        elif 'infrastructure' in labels:
            return 'infrastructure_setup'
        elif 'website' in labels:
            return 'web_development'
        elif 'api' in labels:
            return 'api_integration'
        elif 'testing' in labels:
            return 'testing_validation'
        else:
            return 'general_task'

    def _determine_priority(self, labels: List[str], content: str) -> str:
        """Determine priority based on content and labels."""
        content_lower = content.lower()

        # High priority indicators
        if any(word in content_lower for word in ['urgent', 'critical', 'blocking', 'security']):
            return 'high'
        elif any(word in content_lower for word in ['important', 'priority', 'needed']):
            return 'high'

        # Medium priority for core features
        if any(label in ['agent', 'infrastructure', 'api'] for label in labels):
            return 'medium'

        # Low priority for everything else
        return 'low'

    def _estimate_complexity(self, content: str) -> str:
        """Estimate task complexity based on content length and keywords."""
        content_length = len(content)

        # Complexity indicators
        complexity_keywords = ['complex', 'advanced', 'integration', 'multiple', 'system', 'architecture']

        has_complexity = any(keyword in content.lower() for keyword in complexity_keywords)

        if content_length > 2000 or has_complexity:
            return 'high'
        elif content_length > 1000:
            return 'medium'
        else:
            return 'low'


class GitHubIssueSwarmRunner:
    """Run the swarm on GitHub issues."""

    def __init__(self):
        """Initialize the GitHub issue swarm runner."""
        self.logger = logging.getLogger(__name__)
        self.issue_loader = GitHubIssueLoader()
        self.swarm_manager = None
        self.issues = []
        self.completed_issues = []

    def initialize_swarm(self) -> bool:
        """Initialize the production swarm.

        Returns:
            True if initialization successful
        """
        # Load swarm configuration
        config = SwarmConfig()
        config.max_runtime_hours = 48  # Allow longer runtime for issue processing
        config.monitoring_enabled = True

        # Include ALL swarm agents for collaborative processing
        config.default_agents = [
            'video_editor',
            'audio_engineer',
            'social_media_manager',
            'content_distributor',
            'sponsorship_manager',
            'tour_manager',
            'swarm_orchestrator',
            'communication_liaison',
            'monitoring_overseer',
            'quality_assurance_agent',
            'resource_manager',
            'data_analyst_agent',
            'security_agent'
        ]

        # Enable collaborative features - increase concurrent tasks for parallel processing
        config.max_concurrent_tasks = 5  # Allow multiple tasks to run simultaneously

        # Initialize swarm
        self.swarm_manager = ProductionSwarmManager(config)

        if self.swarm_manager.initialize_swarm():
            self.logger.info("✅ Swarm initialized for GitHub issue processing")
            return True
        else:
            self.logger.error("❌ Swarm initialization failed")
            return False

    def load_github_issues(self) -> bool:
        """Load GitHub issues for processing.

        Returns:
            True if issues loaded successfully
        """
        self.issues = self.issue_loader.load_all_issues()

        if not self.issues:
            self.logger.warning("No GitHub issues found to process")
            return False

        self.logger.info(f"📋 Loaded {len(self.issues)} GitHub issues for processing:")
        for issue in self.issues:
            self.logger.info(f"  - Issue #{issue.get('number', 'N/A')}: {issue['title']} ({issue['priority']} priority)")

        return True

    def assign_issues_as_tasks(self) -> None:
        """Assign GitHub issues as tasks to the swarm."""
        self.logger.info("🎯 Assigning GitHub issues as swarm tasks...")

        assigned_count = 0

        for issue in self.issues:
            # Create task from issue
            task = {
                'id': issue['id'],
                'type': issue['type'],
                'title': issue['title'],
                'description': issue['description'],
                'full_content': issue['full_content'],
                'context': issue['context'],
                'priority': issue['priority'],
                'complexity': issue['estimated_complexity'],
                'labels': issue['labels'],
                'github_issue_number': issue.get('number'),
                'file_path': issue['file_path'],
                'source': 'github_issue'
            }

            # Assign task through collaborative swarm with voting
            assigned_agent = self._assign_task_collaboratively(task)

            if assigned_agent:
                self.logger.info(f"✓ Assigned issue #{issue.get('number', 'N/A')} '{issue['title']}' to {assigned_agent}")
                assigned_count += 1
                issue['assigned_agent'] = assigned_agent
                issue['assigned_at'] = time.time()
            else:
                self.logger.warning(f"✗ No suitable agent found for issue #{issue.get('number', 'N/A')} '{issue['title']}'")

        self.logger.info(f"📊 Assigned {assigned_count}/{len(self.issues)} issues to swarm agents")

    def _assign_task_collaboratively(self, task: Dict[str, Any]) -> str | None:
        """Assign task using collaborative voting and consensus.

        Args:
            task: Task to assign

        Returns:
            Name of assigned agent or None
        """
        # First, let swarm orchestrator analyze and propose assignment
        orchestrator = self.swarm_manager.agents.get('swarm_orchestrator')
        if orchestrator:
            # Get orchestrator's recommendation
            recommendation = self._get_orchestrator_recommendation(orchestrator, task)
            if recommendation:
                self.logger.info(f"🎯 Orchestrator recommends: {recommendation}")

                # Get consensus from relevant agents
                consensus_result = self._build_consensus(task, recommendation)
                if consensus_result:
                    return consensus_result

        # Fallback to standard assignment
        return self.swarm_manager.observability.assign_task(task)

    def _get_orchestrator_recommendation(self, orchestrator, task: Dict[str, Any]) -> str | None:
        """Get assignment recommendation from swarm orchestrator."""
        try:
            # Simulate orchestrator analysis (in real implementation, this would use AI)
            task_type = task.get('type', '')
            context = task.get('context', '')

            # Map task types to preferred agents
            agent_mapping = {
                'agent_implementation': 'swarm_orchestrator',
                'video_processing': 'video_editor',
                'audio_processing': 'audio_engineer',
                'social_media_management': 'social_media_manager',
                'content_distribution': 'content_distributor',
                'infrastructure_setup': 'resource_manager',
                'web_development': 'communication_liaison',
                'api_integration': 'data_analyst_agent',
                'testing_validation': 'quality_assurance_agent',
                'general_task': 'communication_liaison'
            }

            return agent_mapping.get(task_type, 'swarm_orchestrator')

        except Exception as e:
            self.logger.error(f"Error getting orchestrator recommendation: {e}")
            return None

    def _build_consensus(self, task: Dict[str, Any], recommendation: str) -> str | None:
        """Build consensus among agents for task assignment.

        Args:
            task: Task being assigned
            recommendation: Initial recommendation

        Returns:
            Consensus agent assignment or None
        """
        votes = {}
        relevant_agents = self._get_relevant_agents_for_task(task)

        # Collect votes from relevant agents
        for agent_name in relevant_agents:
            agent = self.swarm_manager.agents.get(agent_name)
            if agent:
                try:
                    # Simulate agent voting (in real implementation, this would use AI)
                    vote = self._get_agent_vote(agent, task, recommendation)
                    if vote:
                        votes[agent_name] = vote
                        self.logger.debug(f"🗳️ {agent_name} votes for: {vote}")
                except Exception as e:
                    self.logger.error(f"Error getting vote from {agent_name}: {e}")

        # Count votes
        if votes:
            vote_counts = {}
            for vote in votes.values():
                vote_counts[vote] = vote_counts.get(vote, 0) + 1

            # Find consensus (simple majority)
            max_votes = max(vote_counts.values())
            consensus_candidates = [agent for agent, count in vote_counts.items() if count == max_votes]

            if len(consensus_candidates) == 1:
                consensus = consensus_candidates[0]
                self.logger.info(f"✅ Consensus reached: {consensus} ({max_votes}/{len(votes)} votes)")
                return consensus
            else:
                # Tie - let orchestrator decide
                self.logger.info(f"🤝 Tie between {consensus_candidates}, using orchestrator recommendation")
                return recommendation

        return None

    def _get_relevant_agents_for_task(self, task: Dict[str, Any]) -> List[str]:
        """Get agents relevant to a task for voting."""
        task_type = task.get('type', '')
        context = task.get('context', '')

        # Always include orchestrator and communication liaison
        relevant = ['swarm_orchestrator', 'communication_liaison']

        # Add context-specific agents
        if 'video' in task_type or 'video' in context:
            relevant.extend(['video_editor', 'quality_assurance_agent'])
        elif 'audio' in task_type or 'audio' in context:
            relevant.extend(['audio_engineer', 'quality_assurance_agent'])
        elif 'social' in task_type or 'social' in context:
            relevant.extend(['social_media_manager', 'data_analyst_agent'])
        elif 'content' in task_type or 'content' in context:
            relevant.extend(['content_distributor', 'data_analyst_agent'])
        elif 'agent' in task_type or 'infrastructure' in context:
            relevant.extend(['resource_manager', 'security_agent'])
        elif 'web' in context or 'website' in task_type:
            relevant.extend(['communication_liaison', 'quality_assurance_agent'])

        # Remove duplicates and ensure agents exist
        relevant = list(set(relevant))
        relevant = [agent for agent in relevant if agent in self.swarm_manager.agents]

        return relevant

    def _get_agent_vote(self, agent, task: Dict[str, Any], recommendation: str) -> str | None:
        """Get a vote from an agent for task assignment."""
        try:
            # Simple heuristic-based voting (in real implementation, this would use AI)
            agent_name = agent.agent_name
            task_type = task.get('type', '')

            # Check if agent is specialized for this task
            if task_type in agent.role.lower():
                return agent_name

            # Check tool relevance
            agent_tools = [tool.lower() for tool in agent.get_available_tools()]
            if any(task_type.split('_')[0] in tool for tool in agent_tools):
                return agent_name

            # Default to recommendation if agent has capacity
            return recommendation

        except Exception as e:
            self.logger.error(f"Error getting vote from agent: {e}")
            return None

    def monitor_progress(self) -> None:
        """Monitor swarm progress on GitHub issues."""
        self.logger.info("📊 Monitoring swarm progress on GitHub issues...")

        start_time = time.time()
        last_status_time = 0

        while True:
            current_time = time.time()

            # Update issue status based on swarm tasks
            self._update_issue_status()

            # Log status periodically
            if current_time - last_status_time > 60:  # Every minute
                self._log_current_status()
                last_status_time = current_time

            # Check completion
            if self._all_issues_completed():
                self.logger.info("🎉 All GitHub issues have been processed!")
                break

            # Check for timeout (48 hours)
            if current_time - start_time > 48 * 3600:
                self.logger.warning("⏰ Timeout reached (48 hours), stopping issue processing")
                break

            time.sleep(10)  # Check every 10 seconds

    def _update_issue_status(self) -> None:
        """Update issue status based on swarm task completion."""
        # Get current swarm status
        swarm_status = self.swarm_manager.observability.coordinator.get_swarm_status()

        # Check completed tasks
        for issue in self.issues:
            if issue['status'] == 'open' and issue.get('assigned_agent'):
                task_id = issue['id']

                # Check if task is completed (simplified check)
                # In a real implementation, this would check the actual task completion status
                if task_id not in self.swarm_manager.active_tasks:
                    # Assume completed if not active (simplified)
                    issue['status'] = 'completed'
                    issue['completed_at'] = time.time()
                    self.completed_issues.append(issue)
                    self.logger.info(f"✅ Issue #{issue.get('number', 'N/A')} '{issue['title']}' marked as completed")

    def _log_current_status(self) -> None:
        """Log current processing status."""
        total_issues = len(self.issues)
        completed_count = len(self.completed_issues)
        active_count = len([i for i in self.issues if i['status'] == 'open' and i.get('assigned_agent')])

        swarm_status = self.swarm_manager.get_status()

        self.logger.info(f"📈 Progress: {completed_count}/{total_issues} issues completed, {active_count} active")
        self.logger.info(f"🤖 Swarm: {swarm_status['agents']['active']}/{swarm_status['agents']['total']} agents active")
        self.logger.info(f"⚡ Tasks: {swarm_status['tasks']['active']} active, {swarm_status['tasks']['completed_today']} completed today")

    def _all_issues_completed(self) -> bool:
        """Check if all assignable issues have been completed."""
        # Count issues that were actually assigned to agents
        assigned_issues = [issue for issue in self.issues if issue.get('assigned_agent')]
        return len(self.completed_issues) == len(assigned_issues)

    def generate_completion_report(self) -> Dict[str, Any]:
        """Generate a completion report for the GitHub issues processing."""
        end_time = time.time()

        # Calculate statistics
        total_issues = len(self.issues)
        completed_issues = len(self.completed_issues)
        completion_rate = (completed_issues / total_issues * 100) if total_issues > 0 else 0

        # Group by priority
        priority_stats = {}
        for issue in self.issues:
            priority = issue.get('priority', 'unknown')
            if priority not in priority_stats:
                priority_stats[priority] = {'total': 0, 'completed': 0}
            priority_stats[priority]['total'] += 1
            if issue['status'] == 'completed':
                priority_stats[priority]['completed'] += 1

        # Group by agent assignments
        agent_stats = {}
        for issue in self.completed_issues:
            agent = issue.get('assigned_agent', 'unassigned')
            if agent not in agent_stats:
                agent_stats[agent] = 0
            agent_stats[agent] += 1

        report = {
            'processing_summary': {
                'total_issues': total_issues,
                'completed_issues': completed_issues,
                'completion_rate': completion_rate,
                'processing_time_seconds': end_time - time.time(),  # Would need to track start time
                'average_time_per_issue': (end_time - time.time()) / completed_issues if completed_issues > 0 else 0
            },
            'priority_breakdown': priority_stats,
            'agent_performance': agent_stats,
            'completed_issues': [
                {
                    'number': issue.get('number'),
                    'title': issue['title'],
                    'assigned_agent': issue.get('assigned_agent'),
                    'completed_at': issue.get('completed_at')
                } for issue in self.completed_issues
            ],
            'swarm_final_status': self.swarm_manager.get_status() if self.swarm_manager else {}
        }

        return report

    def run(self) -> None:
        """Run the complete GitHub issue processing workflow."""
        self.logger.info("🚀 Starting Democratic Agent Swarm on GitHub Issues")
        self.logger.info("=" * 80)

        try:
            # Initialize components
            if not self.initialize_swarm():
                return

            if not self.load_github_issues():
                return

            # Assign issues as tasks
            self.assign_issues_as_tasks()

            # Monitor progress until completion
            self.monitor_progress()

            # Generate final report
            report = self.generate_completion_report()
            self.logger.info("📊 Final Report:")
            self.logger.info(json.dumps(report, indent=2, default=str))

        except KeyboardInterrupt:
            self.logger.info("Processing interrupted by user")
        except Exception as e:
            self.logger.error(f"Fatal error during processing: {e}")
            raise
        finally:
            # Cleanup
            if self.swarm_manager:
                self.swarm_manager._shutdown()
            self.logger.info("GitHub issue processing complete")


def main():
    """Main entry point."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/github_issues_swarm_{int(time.time())}.log"),
            logging.StreamHandler()
        ]
    )

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Run the GitHub issue processing
    runner = GitHubIssueSwarmRunner()
    runner.run()


if __name__ == "__main__":
    main()