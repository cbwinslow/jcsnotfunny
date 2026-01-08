import os
import subprocess
import sys
import pytest


def test_production_launcher_dry_run(monkeypatch, tmp_path):
    # Ensure required env vars exist for dry run
    os.environ['GITHUB_TOKEN'] = 'fake'
    os.environ['GITHUB_REPO_OWNER'] = 'owner'
    os.environ['GITHUB_REPO_NAME'] = 'repo'

    # Monkeypatch AutonomousGitHubWorkflow to avoid external calls
    class DummyWorkflow:
        def __init__(self, config_file):
            pass

        def initialize_system(self):
            return True

        @property
        def github_agent(self):
            class G:
                def get_github_issues(self, limit=1):
                    return {'items': []}
            return G()

        @property
        def orchestrator(self):
            class O:
                def analyze_swarm_health(self):
                    return {'overall_health_score': 1.0}
            return O()

    import types
    mod = types.ModuleType('autonomous_github_workflow')
    mod.AutonomousGitHubWorkflow = DummyWorkflow
    sys.modules['autonomous_github_workflow'] = mod

    # Import inside test so monkeypatch applies
    from production_launcher import ProductionConfig, ProductionLauncher

    config = ProductionConfig()
    config.dry_run = True

    # Monkeypatch _validate_github_cli to avoid requiring gh tool
    monkeypatch.setattr(ProductionLauncher, '_validate_github_cli', lambda self: None)

    launcher = ProductionLauncher(config)
    rc = launcher.launch_production_system()
    assert rc == 0
