"""Troubleshooting and testing agent utilities."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from scripts.credential_checks import audit_credentials, summarize_results
from scripts.diagnostics import run_snapshot


@dataclass
class TestRunResult:
    status: str
    returncode: int
    stdout: str
    stderr: str

    def as_dict(self) -> Dict:
        return {
            'status': self.status,
            'returncode': self.returncode,
            'stdout': self.stdout,
            'stderr': self.stderr,
        }


@dataclass
class ConfigCheckResult:
    path: str
    status: str
    details: str = ''

    def as_dict(self) -> Dict:
        return {
            'path': self.path,
            'status': self.status,
            'details': self.details,
        }


@dataclass
class LogScanResult:
    path: str
    status: str
    hits: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            'path': self.path,
            'status': self.status,
            'hits': self.hits,
        }


class TestingAgent:
    __test__ = False
    def __init__(
        self,
        runner: Optional[Callable] = None,
        reader: Optional[Callable[[Path], str]] = None,
    ) -> None:
        self.runner = runner or subprocess.run
        self.reader = reader or (lambda path: path.read_text())

    def run_pytest(self, args: Optional[List[str]] = None) -> TestRunResult:
        cmd = ['python', '-m', 'pytest']
        if args:
            cmd.extend(args)
        proc = self.runner(cmd, capture_output=True, text=True)
        status = 'ok' if proc.returncode == 0 else 'failed'
        return TestRunResult(
            status=status,
            returncode=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
        )

    def validate_config_file(self, path: str) -> ConfigCheckResult:
        target = Path(path)
        if not target.exists():
            return ConfigCheckResult(path=path, status='missing', details='file not found')
        if target.suffix == '.json':
            try:
                json.loads(self.reader(target))
            except json.JSONDecodeError as exc:
                return ConfigCheckResult(path=path, status='invalid', details=str(exc))
            return ConfigCheckResult(path=path, status='ok')
        if target.suffix == '.toml':
            try:
                import tomllib
            except Exception:
                return ConfigCheckResult(path=path, status='skipped', details='tomllib not available')
            try:
                tomllib.loads(self.reader(target))
            except Exception as exc:
                return ConfigCheckResult(path=path, status='invalid', details=str(exc))
            return ConfigCheckResult(path=path, status='ok')
        return ConfigCheckResult(path=path, status='skipped', details='unsupported file type')

    def validate_configs(self, paths: List[str]) -> List[ConfigCheckResult]:
        return [self.validate_config_file(path) for path in paths]

    def scan_logs(self, path: str, limit: int = 20) -> LogScanResult:
        target = Path(path)
        if not target.exists():
            return LogScanResult(path=path, status='missing', hits=[])
        hits: List[str] = []
        lines = self.reader(target).splitlines()
        for line in lines:
            if any(token in line.lower() for token in ('error', 'warning', 'exception', 'failed')):
                hits.append(line)
                if len(hits) >= limit:
                    break
        status = 'ok' if not hits else 'warn'
        return LogScanResult(path=path, status=status, hits=hits)

    def credential_report(self, mode: str = 'offline') -> Dict:
        results = audit_credentials(mode=mode)
        summary = summarize_results(results)
        return {'summary': summary, 'results': [r.as_dict() for r in results]}

    def diagnostics_report(self, live: bool = False) -> Dict:
        return run_snapshot(live=live)

    def build_report(
        self,
        run_pytest: bool = False,
        pytest_args: Optional[List[str]] = None,
        config_paths: Optional[List[str]] = None,
        credential_mode: str = 'offline',
        diagnostics_live: bool = False,
        log_path: str = 'log/codex-tui.log',
    ) -> Dict:
        report: Dict[str, Dict] = {}
        if run_pytest:
            report['pytest'] = self.run_pytest(args=pytest_args).as_dict()
        if config_paths is None or not config_paths:
            default_candidates = [
                'config.json',
                'config.toml',
                'configs/master_settings.json',
                'configs/automation_tools.json',
            ]
            config_paths = [path for path in default_candidates if Path(path).exists()]
        if config_paths:
            report['config_checks'] = [r.as_dict() for r in self.validate_configs(config_paths)]
        report['credentials'] = self.credential_report(mode=credential_mode)
        report['diagnostics'] = self.diagnostics_report(live=diagnostics_live)
        report['log_scan'] = self.scan_logs(log_path).as_dict()
        return report
