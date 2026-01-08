"""Automation runner for thumbnails, SEO, scheduling, and archive manifests."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from scripts.archive_uploader import build_manifest, write_manifest, upload_manifest_s3
from scripts.seo_tools import build_seo_package, write_seo_package
from scripts.social_scheduler import build_schedule, schedule_posts
from scripts.social_workflows import SocialWorkflow
from scripts.thumbnail_agent import extract_keywords, generate_thumbnail_brief


def _load_json(path: Path) -> Dict:
    with path.open('r') as fh:
        return json.load(fh)


def _load_yaml(path: Path) -> Dict:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError('PyYAML is required to load YAML configs') from exc
    with path.open('r') as fh:
        return yaml.safe_load(fh)


def load_config(path: Path) -> Dict:
    if path.suffix == '.json':
        return _load_json(path)
    if path.suffix in ('.yml', '.yaml'):
        return _load_yaml(path)
    raise ValueError(f'Unsupported config format: {path.suffix}')


def load_tools_config(path: Optional[str] = None) -> Dict:
    if path:
        return load_config(Path(path))
    settings = load_master_settings()
    tools_path = settings.get('automation', {}).get('tools_config')
    if tools_path:
        candidate = Path(tools_path)
        if candidate.exists():
            return load_config(candidate)
    candidates = [
        Path('configs/automation_tools.json'),
        Path('configs/automation_tools.yml'),
        Path('configs/automation_tools.yaml'),
    ]
    for candidate in candidates:
        if candidate.exists():
            return load_config(candidate)
    return {}


def load_master_settings(path: Optional[str] = None) -> Dict:
    if path:
        return load_config(Path(path))
    candidates = [
        Path('configs/master_settings.json'),
        Path('configs/master_settings.yml'),
        Path('configs/master_settings.yaml'),
    ]
    for candidate in candidates:
        if candidate.exists():
            return load_config(candidate)
    return {}


def _coerce_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]


def run_automation(
    metadata: Dict,
    summary: Optional[str] = None,
    transcript_path: Optional[str] = None,
    keyframe_paths: Optional[List[str]] = None,
    base_time: Optional[str] = None,
    schedule_offsets: Optional[Dict[str, int]] = None,
    archive_paths: Optional[List[str]] = None,
    tools_config: Optional[Dict] = None,
    execute_schedule: bool = False,
    upload_archive: bool = False,
    report_path: Optional[str] = None,
) -> Dict:
    tools_config = tools_config or load_tools_config()
    summary = summary or metadata.get('summary', '') or ''
    title = metadata.get('title', 'Untitled Episode')
    slug = metadata.get('slug', 'episode')
    results: Dict[str, Dict] = {'metadata': metadata}

    thumbnail_cfg = tools_config.get('thumbnail_agent', {})
    if thumbnail_cfg.get('enabled', True):
        out_dir = thumbnail_cfg.get('output', {}).get('out_dir', 'exports/thumbnails')
        out_path = os.path.join(out_dir, f'{slug}_thumbnail_brief.json')
        brief = generate_thumbnail_brief(
            title=title,
            summary=summary,
            transcript_path=transcript_path,
            keyframe_paths=keyframe_paths,
            out_path=out_path,
        )
        results['thumbnail'] = {'brief_path': out_path, 'prompt': brief.get('prompt')}

    seo_cfg = tools_config.get('seo_assistant', {})
    if seo_cfg.get('enabled', True):
        keywords = metadata.get('keywords')
        if not keywords:
            keywords = extract_keywords(' '.join([title, summary]), limit=seo_cfg.get('keywords_limit', 10))
        seo = build_seo_package(
            title=title,
            summary=summary,
            keywords=keywords,
            canonical_url=metadata.get('canonical_url'),
            og_image_url=metadata.get('thumbnail_url'),
            published_at=metadata.get('published_at'),
            episode_number=metadata.get('episode_number'),
            guest_name=metadata.get('guest'),
        )
        out_dir = seo_cfg.get('output_dir', 'exports/seo')
        out_path = os.path.join(out_dir, f'{slug}.json')
        write_seo_package(seo, out_path)
        results['seo'] = {'path': out_path, 'keywords': keywords}

    scheduler_cfg = tools_config.get('social_scheduler', {})
    if scheduler_cfg.get('enabled', True) and base_time:
        offsets = schedule_offsets or scheduler_cfg.get('default_offsets_minutes', {})
        platforms = metadata.get('platforms') or metadata.get('social_platforms') or []
        schedule = build_schedule(platforms=platforms, base_time=base_time, offsets_minutes=offsets)
        results['schedule'] = {'items': [item.as_dict() for item in schedule]}
        if execute_schedule:
            workflow = SocialWorkflow()
            scheduled = schedule_posts(workflow, metadata, schedule)
            results['schedule']['scheduled'] = scheduled

    archive_cfg = tools_config.get('archive_uploader', {})
    if archive_cfg.get('enabled', True) and archive_paths:
        manifest_path = os.path.join('exports', f'{slug}_archive_manifest.json')
        items = build_manifest(archive_paths, hash_files=True)
        write_manifest(items, manifest_path)
        results['archive'] = {'manifest': manifest_path, 'items': len(items)}
        if upload_archive:
            bucket = os.environ.get(archive_cfg.get('bucket_env', ''), '')
            endpoint = os.environ.get(archive_cfg.get('endpoint_env', ''), '')
            access_key = os.environ.get(archive_cfg.get('access_key_id_env', ''), '')
            secret_key = os.environ.get(archive_cfg.get('secret_access_key_env', ''), '')
            prefix = archive_cfg.get('prefix', 'archive/')
            upload_res = upload_manifest_s3(
                items,
                bucket=bucket,
                endpoint=endpoint,
                access_key=access_key,
                secret_key=secret_key,
                prefix=prefix,
            )
            results['archive']['upload'] = upload_res

    if report_path:
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as fh:
            json.dump(results, fh, indent=2)
        results['report_path'] = report_path

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description='Automation runner')
    parser.add_argument('--metadata', required=True, help='Metadata JSON file')
    parser.add_argument('--summary', default=None)
    parser.add_argument('--transcript', default=None)
    parser.add_argument('--keyframes', default=None, help='Comma-separated keyframe paths')
    parser.add_argument('--base-time', default=None, help='ISO-8601 base publish time')
    parser.add_argument('--offsets', default=None, help='JSON file of platform offsets')
    parser.add_argument('--archive', default=None, help='Comma-separated paths to archive')
    parser.add_argument('--report', default='exports/automation_report.json')
    parser.add_argument('--execute-schedule', action='store_true')
    parser.add_argument('--upload-archive', action='store_true')
    parser.add_argument('--tools-config', default=None)
    args = parser.parse_args()

    metadata = _load_json(Path(args.metadata))
    offsets = None
    if args.offsets:
        offsets = _load_json(Path(args.offsets))
    results = run_automation(
        metadata=metadata,
        summary=args.summary,
        transcript_path=args.transcript,
        keyframe_paths=_coerce_list(args.keyframes),
        base_time=args.base_time,
        schedule_offsets=offsets,
        archive_paths=_coerce_list(args.archive),
        tools_config=load_tools_config(args.tools_config),
        execute_schedule=args.execute_schedule,
        upload_archive=args.upload_archive,
        report_path=args.report,
    )
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
