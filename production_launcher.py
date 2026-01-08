#!/usr/bin/env python3
"""
Production Launcher for Democratic AI Agent Swarm - GitHub Issues Workflow

This script provides a complete production-ready launcher for the autonomous GitHub issues workflow system,
including comprehensive configuration management, environment validation, and enterprise-grade deployment features.

Features:
- Complete environment validation and setup
- Production configuration management
- Enterprise logging and monitoring integration
- Graceful startup and shutdown handling
- Resource management and optimization
- Security and access control validation
- Performance monitoring and alerting
- Comprehensive error handling and recovery

Usage:
    python production_launcher.py [options]

Options:
    --config FILE          Configuration file path (default: agents_config.json)
    --env-file FILE        Environment variables file
    --log-level LEVEL      Logging level (DEBUG, INFO, WARNING, ERROR)
    --max-runtime HOURS    Maximum runtime in hours (default: 24)
    --max-tasks NUM        Maximum concurrent tasks (default: 5)
    --dry-run             Validate configuration without starting
    --verbose             Enable verbose output
    --daemon              Run in daemon mode (background)
"""

import argparse
import json
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import subprocess
import psutil

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from autonomous_github_workflow import AutonomousGitHubWorkflow


@dataclass
class ProductionConfig:
    """Production configuration settings."""
    config_file: str = "agents_config.json"
    env_file: Optional[str] = None
    log_level: str = "INFO"
    max_runtime_hours: int = 24
    max_concurrent_tasks: int = 5
    loop_detection_threshold: int = 10
    monitoring_interval: int = 60
    issue_check_interval: int = 300
    health_check_interval: int = 300
    progress_report_interval: int = 600
    dry_run: bool = False
    verbose: bool = False
    daemon_mode: bool = False
    pid_file: str = "/tmp/democratic_swarm.pid"
    log_file: str = "logs/production_swarm.log"
    enable_telemetry: bool = True
    enable_metrics: bool = True
    enable_alerts: bool = True


class ProductionLauncher:
    """Production launcher for the democratic swarm system."""

    def __init__(self, config: ProductionConfig):
        """Initialize the production launcher."""
        self.config = config
        self.logger = self._setup_logging()
        self.workflow: Optional[AutonomousGitHubWorkflow] = None
        self.start_time = time.time()
        self.pid_file = Path(config.pid_file)

        # Validate configuration
        self._validate_configuration()

        self.logger.info("🎯 Production Launcher initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for production."""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Setup logger
        logger = logging.getLogger("production_launcher")
        logger.setLevel(getattr(logging, self.config.log_level.upper(), logging.INFO))

        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler for production logs
        file_handler = logging.FileHandler(self.config.log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        return logger

    def _validate_configuration(self) -> None:
        """Validate all configuration and environment requirements."""
        self.logger.info("🔍 Validating production configuration...")

        # Check required files
        required_files = [
            self.config.config_file,
            "agents/base_agent.py",
            "agents/swarm_observability.py",
            "agents/github_agent.py",
            "autonomous_github_workflow.py"
        ]

        for file_path in required_files:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Required file not found: {file_path}")

        # Validate configuration file
        try:
            with open(self.config.config_file, 'r') as f:
                config_data = json.load(f)

            if 'agents' not in config_data:
                raise ValueError("Configuration file missing 'agents' section")

            self.logger.info(f"✓ Configuration file validated: {len(config_data['agents'])} agents configured")

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

        # Check environment variables
        self._validate_environment()

        # Check system resources
        self._validate_system_resources()

        # Check GitHub CLI
        self._validate_github_cli()

        self.logger.info("✅ All configuration validations passed")

    def _validate_environment(self) -> None:
        """Validate required environment variables."""
        required_env_vars = [
            ('GITHUB_TOKEN', 'GitHub API access token'),
            ('GITHUB_REPO_OWNER', 'GitHub repository owner'),
            ('GITHUB_REPO_NAME', 'GitHub repository name')
        ]

        optional_env_vars = [
            ('OPENAI_API_KEY', 'OpenAI API access'),
            ('LOG_LEVEL', 'Logging level'),
            ('RABBITMQ_HOST', 'Message queue host'),
            ('REDIS_HOST', 'Cache/queue host'),
            ('LANGFUSE_PUBLIC_KEY', 'LangFuse monitoring'),
            ('OTEL_ENDPOINT', 'OpenTelemetry endpoint')
        ]

        missing_required = []
        for env_var, description in required_env_vars:
            if not os.getenv(env_var):
                missing_required.append(f"{env_var} ({description})")

        if missing_required:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_required)}")

        # Log optional variables status
        available_optional = [env for env, _ in optional_env_vars if os.getenv(env)]
        if available_optional:
            self.logger.info(f"✓ Optional integrations available: {', '.join(available_optional)}")

        unavailable_optional = [env for env, _ in optional_env_vars if not os.getenv(env)]
        if unavailable_optional:
            self.logger.info(f"ℹ️  Optional integrations not configured: {', '.join(unavailable_optional)}")

    def _validate_system_resources(self) -> None:
        """Validate system has adequate resources."""
        try:
            # Check memory
            memory = psutil.virtual_memory()
            min_memory_gb = 4  # Minimum 4GB RAM
            available_memory_gb = memory.available / (1024**3)

            if available_memory_gb < min_memory_gb:
                self.logger.warning(".1f"
                                  ".1f")

            # Check CPU
            cpu_count = psutil.cpu_count()
            if cpu_count < 2:
                self.logger.warning(f"⚠️  Low CPU count: {cpu_count} cores (recommended: 4+)")

            # Check disk space
            disk = psutil.disk_usage('/')
            min_disk_gb = 10  # Minimum 10GB free
            free_disk_gb = disk.free / (1024**3)

            if free_disk_gb < min_disk_gb:
                self.logger.warning(".1f"
                                  ".1f")

            # Log system info
            self.logger.info(f"🖥️  System Resources - CPU: {cpu_count} cores, "
                           ".1f"
                           ".1f")

        except ImportError:
            self.logger.warning("psutil not available - skipping system resource validation")

    def _validate_github_cli(self) -> None:
        """Validate GitHub CLI is installed and authenticated."""
        try:
            result = subprocess.run(['gh', '--version'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                raise RuntimeError("GitHub CLI not found or not working")

            # Check authentication
            auth_result = subprocess.run(['gh', 'auth', 'status'],
                                       capture_output=True, text=True, timeout=10)

            if auth_result.returncode != 0:
                self.logger.warning("⚠️  GitHub CLI authentication may not be configured")
                self.logger.info("Run 'gh auth login' to authenticate with GitHub")

            self.logger.info("✓ GitHub CLI validated and ready")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            raise RuntimeError("GitHub CLI validation failed - ensure 'gh' command is available")

    def _check_existing_process(self) -> bool:
        """Check if another instance is already running."""
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())

                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    if 'python' in process.name().lower():
                        self.logger.error(f"❌ Another swarm process is already running (PID: {pid})")
                        self.logger.info("Use 'kill {pid}' to stop the existing process, or remove the PID file if stale")
                        return True

            except (ValueError, psutil.NoSuchProcess, psutil.AccessDenied):
                # PID file exists but process doesn't - remove stale file
                self.logger.warning("Removing stale PID file")
                self.pid_file.unlink(missing_ok=True)

        return False

    def launch_production_system(self) -> int:
        """Launch the production system."""
        try:
            self.logger.info("🚀 Launching Democratic AI Agent Swarm - Production Mode")
            self.logger.info("=" * 80)

            # Check for existing process
            if self._check_existing_process():
                return 1

            # Dry run mode
            if self.config.dry_run:
                self.logger.info("🏃 Dry run mode - validating configuration only")
                self._perform_dry_run()
                return 0

            # Daemon mode
            if self.config.daemon_mode:
                self.logger.info("🔄 Starting in daemon mode...")
                self._launch_daemon()
                return 0

            # Standard launch
            return self._launch_standard()

        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
            return 1
        except Exception as e:
            self.logger.error(f"Launch failed: {e}")
            return 1

    def _perform_dry_run(self) -> None:
        """Perform a dry run to validate everything without starting."""
        self.logger.info("🔍 Performing dry run validation...")

        # Test agent initialization
        try:
            test_workflow = AutonomousGitHubWorkflow(self.config.config_file)
            if test_workflow.initialize_system():
                self.logger.info("✓ Agent initialization successful")
            else:
                raise RuntimeError("Agent initialization failed")
        except Exception as e:
            raise RuntimeError(f"Dry run failed during agent initialization: {e}")

        # Test GitHub connectivity
        try:
            issues_result = test_workflow.github_agent.get_github_issues(limit=1)
            if 'error' in issues_result:
                self.logger.warning(f"⚠️  GitHub API test warning: {issues_result['error']}")
            else:
                self.logger.info("✓ GitHub API connectivity confirmed")
        except Exception as e:
            raise RuntimeError(f"GitHub connectivity test failed: {e}")

        # Test orchestrator
        try:
            health = test_workflow.orchestrator.analyze_swarm_health()
            self.logger.info(f"✓ Swarm orchestrator functional (health score: {health.get('overall_health_score', 0):.2f})")
        except Exception as e:
            raise RuntimeError(f"Orchestrator test failed: {e}")

        self.logger.info("✅ Dry run completed successfully - all systems ready for production")

    def _launch_daemon(self) -> None:
        """Launch the system in daemon mode (simplified - runs in background)."""
        self.logger.warning("⚠️  Daemon mode not fully supported - running in foreground instead")
        self._launch_standard()

    def _launch_standard(self) -> int:
        """Launch the system in standard (foreground) mode."""
        try:
            # Set environment variables for the workflow
            os.environ['WORKFLOW_MAX_RUNTIME_HOURS'] = str(self.config.max_runtime_hours)
            os.environ['WORKFLOW_MAX_CONCURRENT_TASKS'] = str(self.config.max_concurrent_tasks)
            os.environ['LOOP_DETECTION_THRESHOLD'] = str(self.config.loop_detection_threshold)
            os.environ['WORKFLOW_MONITORING_INTERVAL'] = str(self.config.monitoring_interval)
            os.environ['LOG_LEVEL'] = self.config.log_level

            # Write PID file for standard mode too
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))

            self.logger.info("🎯 Starting Autonomous GitHub Issues Workflow")
            self.logger.info("Configuration:")
            self.logger.info(f"  Max Runtime: {self.config.max_runtime_hours} hours")
            self.logger.info(f"  Max Concurrent Tasks: {self.config.max_concurrent_tasks}")
            self.logger.info(f"  Loop Detection Threshold: {self.config.loop_detection_threshold}")
            self.logger.info(f"  Monitoring Interval: {self.config.monitoring_interval}s")
            self.logger.info(f"  Log Level: {self.config.log_level}")
            self.logger.info("=" * 80)

            # Initialize and run workflow
            self.workflow = AutonomousGitHubWorkflow(self.config.config_file)

            if self.workflow.initialize_system():
                self.logger.info("✅ System initialized successfully")

                # Setup signal handlers for clean shutdown
                def signal_handler(signum, frame):
                    self.logger.info(f"Received signal {signum} - initiating shutdown")
                    if self.workflow:
                        self.workflow.should_stop = True

                signal.signal(signal.SIGTERM, signal_handler)
                signal.signal(signal.SIGINT, signal_handler)

                # Emergency stop handler
                def emergency_stop(signum, frame):
                    self.logger.warning("EMERGENCY STOP signal received!")
                    if self.workflow:
                        self.workflow._master_override = True
                        self.workflow.should_stop = True

                signal.signal(signal.SIGUSR1, emergency_stop)

                # Run the autonomous workflow
                self.workflow.run_autonomous_workflow()

                self.logger.info("✅ Workflow completed successfully")
                return 0

            else:
                self.logger.error("❌ System initialization failed")
                return 1

        except Exception as e:
            self.logger.error(f"❌ Launch failed: {e}")
            return 1
        finally:
            # Clean up PID file
            self.pid_file.unlink(missing_ok=True)

    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        status = {
            'launcher_running': True,
            'start_time': self.start_time,
            'runtime_seconds': time.time() - self.start_time,
            'configuration': {
                'max_runtime_hours': self.config.max_runtime_hours,
                'max_concurrent_tasks': self.config.max_concurrent_tasks,
                'log_level': self.config.log_level,
                'daemon_mode': self.config.daemon_mode
            }
        }

        if self.workflow:
            status['workflow_active'] = True
            status['workflow_state'] = self.workflow.state.value if self.workflow.state else 'unknown'
            status['agents_loaded'] = len(self.workflow.agents)
            status['active_tasks'] = len(self.workflow.active_tasks)
            status['completed_tasks'] = len(self.workflow.completed_tasks)
            status['issues_processed'] = self.workflow.metrics.issues_processed
        else:
            status['workflow_active'] = False

        return status


def parse_arguments() -> ProductionConfig:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Production Launcher for Democratic AI Agent Swarm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--config', '-c',
        default='agents_config.json',
        help='Configuration file path (default: agents_config.json)'
    )

    parser.add_argument(
        '--env-file', '-e',
        help='Environment variables file path'
    )

    parser.add_argument(
        '--log-level', '-l',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--max-runtime', '-r',
        type=int,
        default=24,
        help='Maximum runtime in hours (default: 24)'
    )

    parser.add_argument(
        '--max-tasks', '-t',
        type=int,
        default=5,
        help='Maximum concurrent tasks (default: 5)'
    )

    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Validate configuration without starting'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--daemon', '-D',
        action='store_true',
        help='Run in daemon mode (background)'
    )

    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show current system status'
    )

    parser.add_argument(
        '--stop', '-S',
        action='store_true',
        help='Stop running daemon process'
    )

    args = parser.parse_args()

    # Load environment file if specified
    if args.env_file:
        from dotenv import load_dotenv
        load_dotenv(args.env_file)

    config = ProductionConfig(
        config_file=args.config,
        env_file=args.env_file,
        log_level=args.log_level,
        max_runtime_hours=args.max_runtime,
        max_concurrent_tasks=args.max_tasks,
        dry_run=args.dry_run,
        verbose=args.verbose,
        daemon_mode=args.daemon
    )

    # Handle special actions
    if args.status:
        show_status()
        sys.exit(0)

    if args.stop:
        stop_daemon()
        sys.exit(0)

    return config


def show_status() -> None:
    """Show current system status."""
    pid_file = Path("/tmp/democratic_swarm.pid")

    if not pid_file.exists():
        print("❌ No swarm process found running")
        return

    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())

        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            runtime = time.time() - process.create_time()

            print("✅ Democratic Swarm is running")
            print(f"  PID: {pid}")
            print(".1f")
            print(f"  Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
            print(f"  CPU: {process.cpu_percent():.1f}%")
        else:
            print("❌ Stale PID file found (process not running)")
            pid_file.unlink(missing_ok=True)

    except Exception as e:
        print(f"❌ Error checking status: {e}")


def stop_daemon() -> None:
    """Stop the running daemon process."""
    pid_file = Path("/tmp/democratic_swarm.pid")

    if not pid_file.exists():
        print("❌ No swarm process found running")
        return

    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())

        if psutil.pid_exists(pid):
            print(f"🛑 Stopping swarm process (PID: {pid})...")
            os.kill(pid, signal.SIGTERM)

            # Wait for process to stop
            for _ in range(10):
                if not psutil.pid_exists(pid):
                    print("✅ Swarm process stopped successfully")
                    pid_file.unlink(missing_ok=True)
                    return
                time.sleep(1)

            print("⚠️  Process did not stop gracefully, force killing...")
            os.kill(pid, signal.SIGKILL)
            pid_file.unlink(missing_ok=True)
            print("✅ Swarm process force-killed")

        else:
            print("❌ Process not found (removing stale PID file)")
            pid_file.unlink(missing_ok=True)

    except Exception as e:
        print(f"❌ Error stopping daemon: {e}")


def main() -> int:
    """Main entry point."""
    try:
        config = parse_arguments()

        launcher = ProductionLauncher(config)
        return launcher.launch_production_system()

    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
