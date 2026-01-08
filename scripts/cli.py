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

# Import agent framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
from base_agent import ToolBasedAgent, WorkflowOrchestrator
from transcription_agent import TranscriptionAgent

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
    from scripts.providers.x_client import XClient

    client = XClient()
    res = client.post_text(text)
    click.echo(res)


@cli.command()
@click.option('--mode', type=click.Choice(['offline', 'live']), default='offline')
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), default='text')
def credentials(mode, output_format):
    """Audit credentials for social, streaming, and Cloudflare."""
    from scripts.credential_checks import audit_credentials, format_report, results_to_json

    results = audit_credentials(mode=mode)
    if output_format == 'json':
        click.echo(results_to_json(results))
    else:
        click.echo(format_report(results))


@cli.command()
@click.option('--include-credentials', is_flag=True, default=False)
@click.option('--format', 'output_format', type=click.Choice(['json', 'text']), default='json')
def assistant(include_credentials, output_format):
    """Generate an assistant status report snapshot."""
    from scripts.agent_orchestrator import AgentOrchestrator

    orchestrator = AgentOrchestrator()
    report = orchestrator.status_report(include_credentials=include_credentials)
    if output_format == 'text':
        click.echo(orchestrator.format_report(report))
    else:
        click.echo(json.dumps(report, indent=2))


@cli.command()
@click.option('--run-pytest', is_flag=True, default=False)
@click.option('--pytest-args', default='', help='Comma-separated pytest args')
@click.option('--config', 'config_paths', multiple=True)
@click.option('--credential-mode', type=click.Choice(['offline', 'live']), default='offline')
@click.option('--diagnostics-live', is_flag=True, default=False)
@click.option('--log-path', default='log/codex-tui.log')
@click.option('--format', 'output_format', type=click.Choice(['json', 'text']), default='json')
def troubleshooting(run_pytest, pytest_args, config_paths, credential_mode, diagnostics_live, log_path, output_format):
    """Run troubleshooting checks and emit a report."""
    from scripts.testing_agent import TestingAgent

    agent = TestingAgent()
    report = agent.build_report(
        run_pytest=run_pytest,
        pytest_args=[arg for arg in pytest_args.split(',') if arg] if pytest_args else None,
        config_paths=list(config_paths),
        credential_mode=credential_mode,
        diagnostics_live=diagnostics_live,
        log_path=log_path,
    )
    click.echo(json.dumps(report, indent=2))


# ===== AGENT FRAMEWORK COMMANDS =====

@cli.group()
def agent():
    """Agent framework commands"""
    pass


@agent.command()
@click.option('--agent', 'agent_name', required=True, help='Name of the agent to use')
@click.option('--tool', required=True, help='Tool to execute')
@click.option('--params', required=True, help='JSON parameters for the tool')
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), default='text')
def tool(agent_name, tool, params, output_format):
    """Execute a specific agent tool"""
    try:
        # Parse parameters
        tool_params = json.loads(params)

        # Get agent based on name
        if agent_name == 'transcription':
            agent = TranscriptionAgent()
        else:
            agent = ToolBasedAgent(agent_name)

        # Execute tool
        result = agent.execute_tool(tool, tool_params)

        if output_format == 'json':
            click.echo(json.dumps(result.to_dict(), indent=2))
        else:
            click.echo(f"✅ Tool '{tool}' executed")
            click.echo(f"   Success: {result.success}")
            click.echo(f"   Execution time: {result.execution_time:.2f}s")
            if result.success:
                click.echo(f"   Result: {result.data}")
            else:
                click.echo(f"   Error: {result.error}")
            if result.warnings:
                click.echo(f"   Warnings: {', '.join(result.warnings)}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@agent.command()
@click.option('--agent', 'agent_name', default=None, help='Specific agent to test (optional)')
def test(agent_name, output_format):
    """Test agent functionality"""
    try:
        if agent_name:
            if agent_name == 'transcription':
                agent = TranscriptionAgent()
            else:
                agent = ToolBasedAgent(agent_name)

            status = agent.get_status()
            click.echo(f"Agent: {status['name']}")
            click.echo(f"Role: {status['role']}")
            click.echo(f"Tools: {', '.join(status['available_tools'])}")
            click.echo(f"Success Rate: {status['success_rate']:.1f}%")
        else:
            # Test all agents
            agents_to_test = ['video_editor', 'audio_engineer', 'social_media_manager', 'transcription']

            for agent_name in agents_to_test:
                try:
                    if agent_name == 'transcription':
                        agent = TranscriptionAgent()
                    else:
                        agent = ToolBasedAgent(agent_name)

                    status = agent.get_status()
                    click.echo(f"✅ {agent_name}: {len(status['available_tools'])} tools")
                except Exception as e:
                    click.echo(f"❌ {agent_name}: {str(e)}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@agent.command()
@click.option('--workflow', required=True, help='Workflow name to execute')
@click.option('--params', required=True, help='JSON parameters for the workflow')
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), default='text')
def workflow(workflow, params, output_format):
    """Execute a multi-agent workflow"""
    try:
        # Parse parameters
        workflow_params = json.loads(params)

        # Create orchestrator and execute workflow
        orchestrator = WorkflowOrchestrator()
        result = orchestrator.execute_workflow(workflow, workflow_params)

        if output_format == 'json':
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"Workflow: {result['workflow']}")
            click.echo(f"Success: {result['success']}")
            click.echo(f"Steps executed: {result['steps_executed']}")
            if not result['success']:
                click.echo("Failed steps:")
                for step_name, step_result in result['results'].items():
                    if not step_result['success']:
                        click.echo(f"  - {step_name}: {step_result['error']}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@agent.command()
def list():
    """List available agents and workflows"""
    try:
        orchestrator = WorkflowOrchestrator()

        click.echo("Available Agents:")
        agents = ['video_editor', 'audio_engineer', 'social_media_manager', 'content_distributor', 'sponsorship_manager', 'tour_manager', 'transcription']
        for agent_name in agents:
            try:
                if agent_name == 'transcription':
                    agent = TranscriptionAgent()
                else:
                    agent = ToolBasedAgent(agent_name)
                click.echo(f"  - {agent.name}: {len(agent.get_available_tools())} tools")
            except Exception:
                click.echo(f"  - {agent_name}: (configuration error)")

        click.echo("\nAvailable Workflows:")
        workflows = orchestrator.get_available_workflows()
        for workflow_name in workflows:
            info = orchestrator.get_workflow_info(workflow_name)
            if info:
                click.echo(f"  - {workflow_name}: {info['description']} ({info['steps']} steps)")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


if __name__ == '__main__':
    cli()
