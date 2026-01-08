import importlib.util
import subprocess
import sys
from pathlib import Path


def test_package_agents_script(tmp_path, monkeypatch):
    # Run the packaging script
    script = Path('scripts/package_agents.py')
    assert script.exists()

    ret = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert ret.returncode == 0
    # Check build/agents.tar.gz exists
    assert Path('build/agents.tar.gz').exists()
