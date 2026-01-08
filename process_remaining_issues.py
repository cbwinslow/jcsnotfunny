#!/usr/bin/env python3
"""Process remaining GitHub issues one by one.

This script processes the remaining uncompleted GitHub issues from the swarm run,
processing them individually to ensure each one is properly handled.
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


class SingleIssueProcessor:
    """Process a single GitHub issue through the swarm."""

    def __init__(self, issue_data: Dict[str, Any]):
        """Initialize with issue data."""
        self.issue = issue_data
        self.logger = logging.getLogger(__name__)
        self.swarm_manager: ProductionSwarmManager | None = None
        self.completed = False

    def process_issue(self) -> bool:
        """Process the single issue.

        Returns:
            True if successfully processed
        """
        self.logger.info(f"🎯 Processing issue #{self.issue.get('number', 'N/A')}: {self.issue['title']}")

        try:
            # Initialize swarm for this issue
            if not self._initialize_swarm():
                return False

            # Assign the issue as a task
            if not self._assign_issue():
                return False

            # Monitor until completion or timeout
            if not self._monitor_completion():
                return False

            self.completed = True
            self.logger.info(f"✅ Successfully processed issue #{self.issue.get('number', 'N/A')}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to process issue #{self.issue.get('number', 'N/A')}: {e}")
            return False
        finally:
            if self.swarm_manager:
                self.swarm_manager._shutdown()

    def _initialize_swarm(self) -> bool:
        """Initialize swarm for issue processing."""
        config = SwarmConfig()
        config.max_runtime_hours = 2  # Shorter runtime per issue
        config.monitoring_enabled = True

        # Use relevant agents based on issue context
        context_agents = self._get_relevant_agents()
        config.default_agents = context_agents

        self.swarm_manager = ProductionSwarmManager(config)

        if self.swarm_manager.initialize_swarm():
            self.logger.info(f"✅ Swarm initialized with {len(context_agents)} agents for {self.issue['context']}")
            return True
        else:
            self.logger.error("❌ Swarm initialization failed")
            return False

    def _get_relevant_agents(self) -> List[str]:
        """Get agents relevant to the issue context."""
        context = self.issue.get('context', 'general')

        agent_mapping = {
            'video_editing': ['video_editor', 'swarm_orchestrator', 'quality_assurance_agent'],
            'audio_production': ['audio_engineer', 'swarm_orchestrator', 'quality_assurance_agent'],
            'social_media': ['social_media_manager', 'swarm_orchestrator', 'communication_liaison'],
            'content_distribution': ['content_distributor', 'swarm_orchestrator', 'quality_assurance_agent'],
            'agent_development': ['swarm_orchestrator', 'quality_assurance_agent', 'data_analyst_agent'],
            'infrastructure': ['swarm_orchestrator', 'resource_manager', 'security_agent'],
            'web_development': ['swarm_orchestrator', 'quality_assurance_agent', 'resource_manager'],
            'general': ['swarm_orchestrator', 'communication_liaison', 'quality_assurance_agent']
        }

        return agent_mapping.get(context, agent_mapping['general'])

    def _assign_issue(self) -> bool:
        """Assign the issue as a task."""
        task = {
            'id': self.issue['id'],
            'type': self.issue['type'],
            'title': self.issue['title'],
            'description': self.issue['description'],
            'full_content': self.issue['full_content'],
            'context': self.issue['context'],
            'priority': self.issue['priority'],
            'complexity': self.issue['estimated_complexity'],
            'labels': self.issue['labels'],
            'github_issue_number': self.issue.get('number'),
            'file_path': self.issue['file_path'],
            'source': 'github_issue'
        }

        assigned_agent = self.swarm_manager.observability.assign_task(task)

        if assigned_agent:
            self.logger.info(f"✓ Assigned to {assigned_agent}")
            self.issue['assigned_agent'] = assigned_agent
            self.issue['assigned_at'] = time.time()
            return True
        else:
            self.logger.warning("✗ No suitable agent found")
            return False

    def _monitor_completion(self) -> bool:
        """Monitor until task completion or timeout."""
        start_time = time.time()
        timeout = 3600  # 1 hour per issue

        while time.time() - start_time < timeout:
            # Check if task is completed
            task_id = self.issue['id']
            if task_id not in self.swarm_manager.active_tasks:
                # Check if actually completed by looking at swarm status
                swarm_status = self.swarm_manager.get_status()
                if swarm_status['tasks']['completed_today'] > 0:
                    return True

            time.sleep(30)  # Check every 30 seconds

        self.logger.warning("⏰ Timeout reached for issue processing")
        return False


class RemainingIssuesProcessor:
    """Process remaining GitHub issues one by one."""

    def __init__(self):
        """Initialize the processor."""
        self.logger = logging.getLogger(__name__)
        self.loader = GitHubIssueLoader()
        self.completed_issues = []
        self.failed_issues = []

    def load_remaining_issues(self) -> List[Dict[str, Any]]:
        """Load issues that haven't been completed yet."""
        all_issues = self.loader.load_all_issues()

        # For now, assume all are remaining since we don't have completion tracking
        # In a real scenario, we'd load from a state file
        self.logger.info(f"📋 Loaded {len(all_issues)} issues to process individually")
        return all_issues

    def process_all_remaining(self) -> None:
        """Process all remaining issues one by one."""
        issues = self.load_remaining_issues()

        self.logger.info("🚀 Starting individual issue processing")
        self.logger.info("=" * 80)

        for i, issue in enumerate(issues, 1):
            self.logger.info(f"📊 Processing issue {i}/{len(issues)}")

            processor = SingleIssueProcessor(issue)
            if processor.process_issue():
                self.completed_issues.append(issue)
            else:
                self.failed_issues.append(issue)

            # Brief pause between issues
            time.sleep(5)

        self._generate_report()

    def _generate_report(self) -> None:
        """Generate completion report."""
        total = len(self.completed_issues) + len(self.failed_issues)
        success_rate = (len(self.completed_issues) / total * 100) if total > 0 else 0

        self.logger.info("📊 Processing Complete")
        self.logger.info(f"✅ Completed: {len(self.completed_issues)}")
        self.logger.info(f"❌ Failed: {len(self.failed_issues)}")
        self.logger.info(f"📈 Success Rate: {success_rate:.1f}%")

        if self.failed_issues:
            self.logger.info("Failed issues:")
            for issue in self.failed_issues:
                self.logger.info(f"  - #{issue.get('number', 'N/A')}: {issue['title']}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Process GitHub issues individually')
    parser.add_argument('--issue', type=str, help='Specific issue file to process (e.g., 001-transcription-agent.md)')
    parser.add_argument('--all', action='store_true', help='Process all remaining issues')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/remaining_issues_{int(time.time())}.log"),
            logging.StreamHandler()
        ]
    )

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    processor = RemainingIssuesProcessor()

    if args.issue:
        # Process specific issue
        issues = processor.load_remaining_issues()
        issue = next((i for i in issues if i['file_path'].endswith(args.issue)), None)
        if issue:
            single_processor = SingleIssueProcessor(issue)
            success = single_processor.process_issue()
            print(f"{'✅' if success else '❌'} Processed {args.issue}")
        else:
            print(f"❌ Issue {args.issue} not found")
    elif args.all:
        # Process all remaining issues
        processor.process_all_remaining()
    else:
        # List available issues
        issues = processor.load_remaining_issues()
        print("Available issues:")
        for issue in issues:
            print(f"  - {Path(issue['file_path']).name}: {issue['title']}")
        print("\nUse --issue <filename> to process a specific issue, or --all to process all")


if __name__ == "__main__":
    main()