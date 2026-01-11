# Pydantic AI Swarm Examples

This directory contains examples demonstrating how to use the Pydantic AI Democratic Agent Swarm system.

## Available Examples

### 📁 `simple_swarm_demo.py`
Basic demonstration of swarm functionality:
- Start/stop swarm lifecycle
- Single agent task execution
- Error handling scenarios

**Run:**
```bash
python examples/simple_swarm_demo.py
```

### 📁 `comprehensive_swarm_demo.py`
Complete feature demonstration:
- Multi-agent coordination
- Democratic task assignment
- Health monitoring
- Performance analytics
- Diagnostic capabilities

**Run:**
```bash
python examples/comprehensive_swarm_demo.py
```

## CLI Usage Examples

### Start a Swarm
```bash
# Start basic swarm with 1 agent
python pydantic_swarm_cli.py start --name MySwarm

# Start swarm with 3 agents
python pydantic_swarm_cli.py start --name ProductionSwarm --agents 3
```

### Execute Tasks
```bash
# Basic task execution
python pydantic_swarm_cli.py execute "Analyze this video content"

# Domain-specific task
python pydantic_swarm_cli.py execute "Edit podcast video" --domain video_editing

# High priority task
python pydantic_swarm_cli.py execute "Urgent content optimization" --priority high
```

### Monitoring & Diagnostics
```bash
# Check swarm status
python pydantic_swarm_cli.py status

# Run diagnostics
python pydantic_swarm_cli.py diagnose

# Run demo scenarios
python pydantic_swarm_cli.py demo --scenario multi-agent
```

## Environment Setup

Before running examples, ensure you have:

1. **OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Optional Environment Variables**:
   ```bash
   export PYDANTIC_AI_LOG_LEVEL="INFO"
   export SWARM_NAME="MySwarm"
   ```

## Example Output

Running `simple_swarm_demo.py` should produce output like:

```
Pydantic AI Democratic Swarm - Simple Demo Suite
==================================================

==================== Basic Swarm ====================
=== Pydantic AI Swarm - Basic Demo ===
ERROR: Please set OPENAI_API_KEY environment variable
Basic Swarm: FAILED

==================== Multi-Agent ====================
Multi-Agent Demo
=================
ERROR: Please set OPENAI_API_KEY environment variable
Multi-Agent: FAILED

==================== Error Handling ====================
Error Handling Demo
===================
ERROR: Please set OPENAI_API_KEY environment variable
Error Handling: FAILED

=== Demo Results ===
Passed: 0/3

Some demos failed
```

Once you set the API key, you'll see successful execution with swarm operations, task completions, and health metrics.

## Writing Your Own Examples

### Basic Template

```python
import asyncio
from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent

async def my_example():
    # Create and start swarm
    swarm = PydanticAISwarmOrchestrator("MyExample")
    agent = PydanticVideoEditorAgent("example_agent")

    await swarm.register_agent(agent)
    await swarm.start_swarm()

    # Execute your tasks
    result = await swarm.execute_task("Your task here", {"domain": "video_editing"})

    # Clean up
    await swarm.stop_swarm()

if __name__ == "__main__":
    asyncio.run(my_example())
```

### Advanced Example

```python
from agents.diagnostic_system import SwarmDiagnosticSystem

async def advanced_example():
    swarm = PydanticAISwarmOrchestrator("AdvancedExample")

    # Add multiple agents
    agents = [PydanticVideoEditorAgent(f"agent_{i}") for i in range(3)]
    for agent in agents:
        await swarm.register_agent(agent)

    await swarm.start_swarm()

    # Initialize diagnostics
    diagnostics = SwarmDiagnosticSystem(swarm)
    await diagnostics.start_monitoring()

    # Run tasks and monitor
    for task in ["Task 1", "Task 2", "Task 3"]:
        result = await swarm.execute_task(task, {"domain": "video_editing"})
        print(f"Task result: {result.success}")

    # Check diagnostics
    issues = await diagnostics.run_diagnostics()
    print(f"Found {len(issues)} issues")

    # Generate report
    report = await swarm.generate_performance_report()
    print(f"Tasks processed: {report['summary_metrics']['total_tasks']}")

    # Cleanup
    await diagnostics.stop_monitoring()
    await swarm.stop_swarm()
```

## Best Practices

1. **Always check for API keys** before starting swarms
2. **Use try/finally blocks** for proper cleanup
3. **Monitor swarm health** during operation
4. **Handle exceptions gracefully**
5. **Log important operations** for debugging

## Troubleshooting

### Common Issues

- **"Module not found"**: Ensure you're in the correct directory and virtual environment
- **"API key not set"**: Set the `OPENAI_API_KEY` environment variable
- **"Swarm not active"**: Call `start_swarm()` before executing tasks
- **"Agent failures"**: Check agent configurations and network connectivity

### Getting Help

- Check the main [documentation](../PYDANTIC_AI_SWARM_DOCUMENTATION.md)
- Run diagnostics: `python pydantic_swarm_cli.py diagnose`
- Check logs in the `logs/` directory
- Open an issue on GitHub

---

**Ready to build your own AI swarms?** Start with the simple demo and explore the comprehensive documentation!
