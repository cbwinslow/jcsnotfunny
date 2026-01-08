"""Assistant orchestrator for production status and workflow summaries."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from scripts.credential_checks import audit_credentials, summarize_results

SETTINGS_CANDIDATES = [
    Path('configs/master_settings.json'),
    Path('configs/master_settings.yml'),
    Path('configs/master_settings.yaml'),
]

PROFILES_CANDIDATES = [
    Path('configs/host_profiles.yml'),
    Path('configs/host_profiles.yaml'),
]

AUDIO_PRESETS_CANDIDATES = [
    Path('configs/audio_presets.yml'),
    Path('configs/audio_presets.yaml'),
]


def _load_yaml(path: Path) -> Optional[Dict]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    with path.open('r') as fh:
        return yaml.safe_load(fh)


def _load_json(path: Path) -> Optional[Dict]:
    with path.open('r') as fh:
        return json.load(fh)


def load_settings() -> Optional[Dict]:
    for path in SETTINGS_CANDIDATES:
        if path.exists():
            if path.suffix == '.json':
                return _load_json(path)
            if path.suffix in ('.yml', '.yaml'):
                return _load_yaml(path)
    return None


def load_profiles() -> Optional[Dict]:
    for path in PROFILES_CANDIDATES:
        if path.exists():
            return _load_yaml(path)
    return None


def load_audio_presets() -> Optional[Dict]:
    for path in AUDIO_PRESETS_CANDIDATES:
        if path.exists():
            return _load_yaml(path)
    return None


def parse_open_tasks(path: Path = Path('tasks.md'), limit: int = 20) -> List[str]:
    if not path.exists():
        return []
    tasks: List[str] = []
    with path.open('r') as fh:
        for line in fh:
            raw = line.strip()
            if raw.startswith('- [ ]'):
                tasks.append(raw[5:].strip())
            if len(tasks) >= limit:
                break
    return tasks


def parse_sops_index(path: Path = Path('docs/SOPS.md')) -> List[str]:
    if not path.exists():
        return []
    entries: List[str] = []
    with path.open('r') as fh:
        for line in fh:
            raw = line.strip()
            if raw.startswith('- `docs/'):
                entries.append(raw.split('`')[1])
    return entries


@dataclass
class AssistantReport:
    timestamp: str
    settings_loaded: bool
    profiles_loaded: bool
    audio_presets_loaded: bool
    automation_config_loaded: bool
    automation_config_path: Optional[str]
    sops_docs: List[str]
    open_tasks_sample: List[str] = field(default_factory=list)
    open_tasks_count: int = 0
    credential_summary: Optional[Dict[str, int]] = None
    notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'settings_loaded': self.settings_loaded,
            'profiles_loaded': self.profiles_loaded,
            'audio_presets_loaded': self.audio_presets_loaded,
            'automation_config_loaded': self.automation_config_loaded,
            'automation_config_path': self.automation_config_path,
            'sops_docs': self.sops_docs,
            'open_tasks_count': self.open_tasks_count,
            'open_tasks_sample': self.open_tasks_sample,
            'credential_summary': self.credential_summary,
            'notes': self.notes,
        }


class AgentOrchestrator:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.profiles = load_profiles()
        self.audio_presets = load_audio_presets()

    def status_report(self, include_credentials: bool = False) -> Dict:
        notes: List[str] = []
        if self.settings is None:
            notes.append('settings_not_loaded')
        if self.profiles is None:
            notes.append('profiles_not_loaded')
        if self.audio_presets is None:
            notes.append('audio_presets_not_loaded')

        automation_path = None
        automation_loaded = False
        if self.settings:
            automation_path = self.settings.get('automation', {}).get('tools_config')
            if automation_path and Path(automation_path).exists():
                automation_loaded = True
        if not automation_loaded:
            notes.append('automation_tools_not_loaded')

        sops_docs = parse_sops_index()
        open_tasks = parse_open_tasks()
        report = AssistantReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            settings_loaded=self.settings is not None,
            profiles_loaded=self.profiles is not None,
            audio_presets_loaded=self.audio_presets is not None,
            automation_config_loaded=automation_loaded,
            automation_config_path=automation_path,
            sops_docs=sops_docs,
            open_tasks_sample=open_tasks,
            open_tasks_count=len(open_tasks),
            notes=notes,
        )
        if include_credentials:
            results = audit_credentials(mode='offline')
            report.credential_summary = summarize_results(results)
        return report.as_dict()

    def format_report(self, report: Dict) -> str:
        lines = [
            f"timestamp: {report.get('timestamp')}",
            f"settings_loaded: {report.get('settings_loaded')}",
            f"profiles_loaded: {report.get('profiles_loaded')}",
            f"audio_presets_loaded: {report.get('audio_presets_loaded')}",
            f"automation_config_loaded: {report.get('automation_config_loaded')}",
            f"sops_docs: {len(report.get('sops_docs', []))}",
            f"open_tasks_count: {report.get('open_tasks_count')}",
        ]
        if report.get('credential_summary'):
            summary = report['credential_summary']
            lines.append(f"credential_summary: {summary}")
        if report.get('notes'):
            lines.append(f"notes: {', '.join(report['notes'])}")
        return '\n'.join(lines)
