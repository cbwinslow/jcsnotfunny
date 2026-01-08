from pathlib import Path

from scripts.testing_agent import TestingAgent


class DummyProc:
    def __init__(self, returncode=0, stdout="ok", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_testing_agent_run_pytest():
    def fake_runner(cmd, capture_output=True, text=True):
        assert cmd[:2] == ["python", "-m"]
        return DummyProc(returncode=0, stdout="passed", stderr="")

    agent = TestingAgent(runner=fake_runner)
    result = agent.run_pytest()
    assert result.status == "ok"
    assert "passed" in result.stdout


def test_testing_agent_config_validation(tmp_path):
    json_path = tmp_path / "config.json"
    json_path.write_text('{"ok": true}')
    toml_path = tmp_path / "config.toml"
    toml_path.write_text("key = 'value'")
    agent = TestingAgent()
    results = agent.validate_configs([str(json_path), str(toml_path)])
    assert results[0].status == "ok"
    assert results[1].status == "ok"


def test_testing_agent_log_scan(tmp_path):
    log_path = tmp_path / "log.txt"
    log_path.write_text("INFO ok\nWARNING something\nERROR broken\n")
    agent = TestingAgent()
    result = agent.scan_logs(str(log_path))
    assert result.status == "warn"
    assert len(result.hits) == 2
