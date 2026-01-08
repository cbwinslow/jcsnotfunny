from scripts.agent_orchestrator import AgentOrchestrator, parse_open_tasks


def test_parse_open_tasks(tmp_path):
    tasks_file = tmp_path / "tasks.md"
    tasks_file.write_text("- [ ] First task\n- [x] Done task\n- [ ] Second task\n")
    tasks = parse_open_tasks(path=tasks_file, limit=10)
    assert tasks == ["First task", "Second task"]


def test_agent_orchestrator_report():
    orchestrator = AgentOrchestrator()
    report = orchestrator.status_report(include_credentials=False)
    assert "timestamp" in report
    assert "sops_docs" in report
    assert "open_tasks_count" in report
