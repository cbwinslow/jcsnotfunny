"""Diagnostics and monitoring utilities for streams and recording health."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

from scripts.agent_orchestrator import load_settings
from scripts.credential_checks import STREAMING_TARGETS
from scripts.social_workflows import load_dotenv


@dataclass
class CheckResult:
    name: str
    status: str
    details: str = ''
    value: Optional[float] = None

    def as_dict(self) -> Dict:
        return {
            'name': self.name,
            'status': self.status,
            'details': self.details,
            'value': self.value,
        }


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_rtmp_url(url: str) -> Tuple[Optional[str], Optional[int], str]:
    parsed = urlparse(url)
    host = parsed.hostname
    scheme = parsed.scheme or 'rtmp'
    port = parsed.port
    if port is None:
        port = 443 if scheme == 'rtmps' else 1935
    return host, port, scheme


def _tcp_connect(host: str, port: int, timeout: float = 3.0) -> float:
    start = time.monotonic()
    sock = socket.create_connection((host, port), timeout=timeout)
    sock.close()
    return (time.monotonic() - start) * 1000.0


def _collect_rtmp_urls(settings: Optional[Dict]) -> Dict[str, str]:
    urls: Dict[str, str] = {}
    if settings and isinstance(settings, dict):
        destinations = settings.get('streaming', {}).get('destinations', {})
        for name, config in destinations.items():
            if not isinstance(config, dict):
                continue
            env_key = config.get('rtmp_url_env')
            if env_key and os.environ.get(env_key):
                urls[name] = os.environ[env_key]
    if urls:
        return urls
    for name, (rtmp_key, _stream_key) in STREAMING_TARGETS.items():
        url = os.environ.get(rtmp_key)
        if url:
            urls[name] = url
    return urls


def check_stream_endpoints(
    urls: Dict[str, str],
    live: bool = False,
    connector=_tcp_connect,
) -> List[CheckResult]:
    results: List[CheckResult] = []
    for name, url in urls.items():
        host, port, scheme = _parse_rtmp_url(url)
        if not host or not port:
            results.append(CheckResult(name=name, status='invalid', details='bad rtmp url'))
            continue
        if not live:
            results.append(CheckResult(name=name, status='ok', details='skipped (offline)'))
            continue
        try:
            latency_ms = connector(host, port)
        except OSError as exc:
            results.append(CheckResult(name=name, status='failed', details=str(exc)))
            continue
        status = 'ok'
        detail = f'{scheme} {host}:{port} {latency_ms:.0f}ms'
        if latency_ms > 500:
            status = 'warn'
        results.append(CheckResult(name=name, status=status, details=detail, value=latency_ms))
    return results


def check_disk_space(paths: Iterable[str], min_free_gb: float = 50.0) -> List[CheckResult]:
    results: List[CheckResult] = []
    for path in paths:
        if not path:
            continue
        target = path if os.path.exists(path) else os.path.dirname(path)
        if not target or not os.path.exists(target):
            results.append(CheckResult(name=path, status='missing', details='path not found'))
            continue
        usage = shutil.disk_usage(target)
        free_gb = usage.free / (1024 ** 3)
        status = 'ok' if free_gb >= min_free_gb else 'warn'
        results.append(
            CheckResult(
                name=path,
                status=status,
                details=f'free {free_gb:.1f} GB',
                value=free_gb,
            )
        )
    return results


def check_obs_process() -> CheckResult:
    try:
        if os.name == 'nt':
            cmd = ['tasklist']
        else:
            cmd = ['ps', '-A']
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = proc.stdout.lower()
        if 'obs' in output or 'obs64' in output:
            return CheckResult(name='obs_process', status='ok', details='obs detected')
        return CheckResult(name='obs_process', status='warn', details='obs not detected')
    except Exception as exc:
        return CheckResult(name='obs_process', status='unknown', details=str(exc))


def check_recording_file(path: Optional[str], min_growth_kb: float = 256.0) -> CheckResult:
    if not path:
        return CheckResult(name='recording_file', status='skipped', details='no path provided')
    if not os.path.exists(path):
        return CheckResult(name='recording_file', status='missing', details='file not found')
    size_kb = os.path.getsize(path) / 1024.0
    status = 'ok' if size_kb >= min_growth_kb else 'warn'
    return CheckResult(
        name='recording_file',
        status=status,
        details=f'size {size_kb:.1f} KB',
        value=size_kb,
    )


def check_network_interfaces() -> List[CheckResult]:
    path = '/proc/net/dev'
    if not os.path.exists(path):
        return [CheckResult(name='network', status='skipped', details='unsupported platform')]
    results: List[CheckResult] = []
    with open(path, 'r') as fh:
        lines = fh.read().splitlines()[2:]
    for line in lines:
        if ':' not in line:
            continue
        name, data = line.split(':', 1)
        fields = data.split()
        if len(fields) < 16:
            continue
        rx_bytes = int(fields[0])
        tx_bytes = int(fields[8])
        results.append(
            CheckResult(
                name=f'net:{name.strip()}',
                status='ok',
                details=f'rx={rx_bytes} tx={tx_bytes}',
                value=float(rx_bytes + tx_bytes),
            )
        )
    return results


def run_snapshot(
    live: bool = False,
    env_path: str = '.env',
    recording_file: Optional[str] = None,
) -> Dict:
    load_dotenv(env_path, override=False)
    settings = load_settings()

    paths: List[str] = []
    if settings:
        paths.extend(
            [
                settings.get('paths', {}).get('recordings_dir', ''),
                settings.get('paths', {}).get('exports_dir', ''),
            ]
        )
    else:
        paths.append('recordings')
        paths.append('exports')

    snapshot = {
        'timestamp': _now_iso(),
        'disk': [r.as_dict() for r in check_disk_space(paths)],
        'obs': check_obs_process().as_dict(),
        'network': [r.as_dict() for r in check_network_interfaces()],
        'recording': check_recording_file(recording_file).as_dict(),
    }
    urls = _collect_rtmp_urls(settings)
    snapshot['stream_endpoints'] = [r.as_dict() for r in check_stream_endpoints(urls, live=live)]
    snapshot['notes'] = ['live_checks_enabled' if live else 'offline_mode']
    return snapshot


def format_snapshot(snapshot: Dict) -> str:
    lines = [f"timestamp: {snapshot.get('timestamp')}"]
    lines.append(f"obs: {snapshot.get('obs', {}).get('status')}")
    lines.append(f"recording: {snapshot.get('recording', {}).get('status')}")
    for item in snapshot.get('disk', []):
        lines.append(f"disk:{item['name']}: {item['status']} {item.get('details','')}")
    for item in snapshot.get('stream_endpoints', []):
        lines.append(f"stream:{item['name']}: {item['status']} {item.get('details','')}")
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Diagnostics for stream and recording health')
    parser.add_argument('--live', action='store_true', help='Run live network checks')
    parser.add_argument('--env', default='.env', help='Path to env file')
    parser.add_argument('--recording-file', default=None, help='Path to recording file to inspect')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    snapshot = run_snapshot(live=args.live, env_path=args.env, recording_file=args.recording_file)
    if args.format == 'json':
        print(json.dumps(snapshot, indent=2))
    else:
        print(format_snapshot(snapshot))


if __name__ == '__main__':
    main()
