"""Command-line interface for jcsnotfunny agent toolset

Usage examples:
  python -m scripts.cli transcribe --input raw_videos/ep01/audio_master.wav --output edited/ep01/transcript.vtt
  python -m scripts.cli clips --input raw_videos/ep01/ep01.mp4 --transcript edited/ep01/transcript.vtt --outdir edited/ep01/clips
  python -m scripts.cli publish --video edited/ep01/ep01-final.mp4 --title "Ep 01" --slug ep01
  python -m scripts.cli social --issue 12 --platforms x,instagram --dry-run

This CLI wraps the agents and provides convenience functions, validation and dry-run support.
"""
import json
import os
import sys
import click
from scripts import transcribe, clip_generator, publish, mcp_publish
from scripts.social_publish import render_post
from scripts.providers.x_client import XClient

@click.group()
def cli():
    """Jared's Not Funny CLI"""
    pass

@cli.command()
@click.option('--input', '-i', 'input_file', required=True)
@click.option('--output', '-o', 'output_file', required=True)
@click.option('--backend', default=None, help='transcribe backend override')
def transcribe_cmd(input_file, output_file, backend):
    """Transcribe audio to WebVTT"""
    if backend:
        os.environ['TRANSCRIBE_BACKEND'] = backend
    click.echo(f"Transcribing {input_file} -> {output_file}")
    transcribe.transcribe_with_whisper(input_file, output_file)
    click.echo('Done')

@cli.command()
@click.option('--input', '-i', 'input_video', required=True)
@click.option('--transcript', '-t', 'transcript', required=True)
@click.option('--outdir', '-o', 'outdir', required=True)
def clips(input_video, transcript, outdir):
    """Generate clips from video using transcript"""
    click.echo(f"Generating clips from {input_video} using {transcript}")
    clip_generator.main_args = lambda: None  # compatibility in case
    clip_generator.main.__call__ = None
    # call entrypoint
    # Use the library function to generate clips
    clip_generator.generate_clips(input_video, transcript, outdir)

@cli.command()
@click.option('--video', required=True)
@click.option('--title', required=True)
@click.option('--slug', required=True)
@click.option('--description', default='')
def publish_cmd(video, title, slug, description):
    md = {'title': title, 'slug': slug, 'guest': 'TBD', 'youtube_url': None}
    target = publish.push_episode_to_website(md, 'website/content/episodes')
    click.echo(f'Wrote metadata to {target}')

@cli.command()
@click.option('--mode', type=click.Choice(['api','mcp']), default='api')
@click.option('--endpoint', default='')
@click.option('--platforms', required=True)
@click.option('--metadata', required=True)
@click.option('--api-key', default='')
@click.option('--dry-run', is_flag=True)
def social(mode, endpoint, platforms, metadata, api_key, dry_run):
    """Render and publish social posts using MCP or API mode"""
    platforms_list = [p.strip() for p in platforms.split(',') if p.strip()]
    with open(metadata, 'r') as fh:
        md = json.load(fh)
    if dry_run:
        click.echo('Render preview:')
        for p in platforms_list:
            click.echo('--- ' + p)
            click.echo(render_post(p, md))
        return
    if mode == 'mcp':
        out = mcp_publish.publish_via_mcp(endpoint, api_key or os.environ.get('MCP_API_KEY'), platforms_list, md)
    else:
        out = mcp_publish.publish_via_api(platforms_list, md)
    click.echo(json.dumps(out, indent=2))

@cli.command()
@click.option('--text', default='Hello world')
def post_x_demo(text):
    """Quick demo: post to X via XClient (stub)"""
    client = XClient()
    res = client.post_text(text)
    click.echo(res)

if __name__ == '__main__':
    cli()
