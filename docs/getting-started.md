# Getting Started with Pydantic AI Democratic Agent Swarm

Welcome to the Pydantic AI Democratic Agent Swarm! This guide will walk you through installing, configuring, and running your first democratic AI agent swarm.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed on your system
- **OpenAI API Key** for AI agent functionality
- **Git** for cloning the repository
- **Virtual environment** support (venv)

## 🚀 Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/pydantic-ai-swarm.git
cd pydantic-ai-swarm
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install Pydantic AI
pip install pydantic-ai

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_ORG_ID=your-org-id-optional

# Swarm Configuration
PYDANTIC_AI_LOG_LEVEL=INFO
SWARM_NAME=MyFirstSwarm

# Optional: Advanced settings
PYDANTIC_AI_MODEL=gpt-4o
PYDANTIC_AI_TEMPERATURE=0.7
```

## 🎯 Your First Swarm

### Hello World Example

Create a file called `hello_swarm.py`:

```python
#!/usr/bin/env python3
"""Hello World example for Pydantic AI Swarm."""

import asyncio
from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator
from agents.pydantic_video_editor_agent import PydanticVideoEditorAgent

async def main():
    """Run a simple swarm example."""
    print("🚀 Starting Pydantic AI Democratic Swarm...")

    # Create swarm orchestrator
    swarm = PydanticAISwarmOrchestrator("HelloSwarm")

    # Create and register a video editing agent
    video_agent = PydanticVideoEditorAgent("video_specialist")
    await swarm.register_agent(video_agent)

    # Start the swarm
    await swarm.start_swarm()
    print("✅ Swarm started successfully!")

    # Execute a simple task
    result = await swarm.execute_task(
        "Analyze this sample video content",
        {
            "domain": "video_editing",
            "priority": "normal",
            "content_type": "analysis"
        }
    )

    # Display results
    print(f"📊 Task Result: {'Success' if result.success else 'Failed'}")
    if result.success:
        print(f"📝 Result data: {result.data}")
    else:
        print(f"❌ Error: {result.error}")

    # Get swarm health
    health = await swarm.analyze_swarm_health()
    print(f"🏥 Swarm Health: {health['overall_health_score']:.2f}")

    # Clean shutdown
    await swarm.stop_swarm()
    print("🛑 Swarm stopped. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
```

Run your first swarm:

```bash
python hello_swarm.py
```

You should see output similar to:

```
🚀 Starting Pydantic AI Democratic Swarm...
✅ Swarm started successfully!
📊 Task Result: Success
📝 Result data: {...}
🏥 Swarm Health: 0.95
🛑 Swarm stopped. Goodbye!
```

## 🏗️ Understanding the Components

### Agents

Agents are specialized AI entities with:

- **Domain Expertise**: Specific areas of knowledge (video editing, audio, social media, etc.)
- **Confidence Metrics**: Self-assessment of decision quality
- **Tool Integration**: Access to validated tools
- **Democratic Participation**: Voting rights in swarm decisions

```python
# Create different types of agents
video_agent = PydanticVideoEditorAgent("video_editor")
audio_agent = PydanticAIAgent("audio_specialist", config=audio_config)
social_agent = PydanticAIAgent("social_media_expert", config=social_config)
```

### Swarm Orchestrator

The swarm orchestrator manages:

- **Agent Coordination**: Democratic task assignment
- **Health Monitoring**: Real-time system status
- **Consensus Building**: Voting and decision making
- **Communication**: Inter-agent messaging

```python
# Create and configure swarm
swarm = PydanticAISwarmOrchestrator(
    swarm_name="MyProductionSwarm",
    enable_diagnostics=True,
    enable_monitoring=True,
    voting_timeout_seconds=300
)
```

### Tasks and Execution

Tasks are executed through democratic coordination:

```python
# Simple task
result = await swarm.execute_task("Edit this video", {"domain": "video_editing"})

# Complex task with context
result = await swarm.execute_task(
    "Create a complete social media campaign",
    {
        "domain": "video_editing",
        "platforms": ["tiktok", "instagram"],
        "deadline": "2024-12-31",
        "priority": "high"
    }
)
```

## 📊 Monitoring Your Swarm

### Health Monitoring

```python
# Get comprehensive health status
health = await swarm.analyze_swarm_health()

print("Swarm Health Report:")
print(f"Overall Score: {health['overall_health_score']:.2f}")
print(f"Active Agents: {health['detailed_analysis']['agents']['active']}")
print(f"Task Success Rate: {health['detailed_analysis']['tasks']['success_rate']:.2f}")

# Check for critical issues
if health['critical_issues']:
    print("⚠️ Critical Issues Found:")
    for issue in health['critical_issues']:
        print(f"  - {issue['title']}: {issue['description']}")
```

### Performance Metrics

```python
# Get performance report
report = await swarm.generate_performance_report()

print("Performance Summary:")
print(f"Tasks Processed: {report['summary_metrics']['total_tasks']}")
print(f"Success Rate: {report['summary_metrics']['success_rate']:.2f}")
print(f"Average Duration: {report['summary_metrics']['average_task_duration']:.2f}s")

# View recommendations
if report['recommendations']:
    print("💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")
```

## 🔧 Configuration

### Basic Configuration

The system uses environment variables and configuration files:

```python
# Environment variables
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
os.environ['PYDANTIC_AI_LOG_LEVEL'] = 'INFO'

# Agent configuration
agent_config = AgentConfig(
    name="my_agent",
    role="Video Editor",
    model="gpt-4o",
    domain_expertise=["video_editing", "content_creation"],
    voting_enabled=True
)
```

### Advanced Configuration

```python
# Swarm configuration
swarm_config = {
    "name": "ProductionSwarm",
    "max_concurrent_tasks": 10,
    "health_check_interval": 60,
    "voting_timeout": 300,
    "enable_diagnostics": True,
    "enable_monitoring": True,
    "log_level": "INFO"
}

# Tool configuration
tool_config = ToolConfig(
    enable_caching=True,
    cache_ttl_seconds=600,
    max_retries=3,
    timeout_seconds=120
)
```

## 🧪 Testing Your Setup

### Run the Test Suite

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific tests
pytest tests/test_pydantic_ai_system.py::TestPydanticAIModels -v

# Run with coverage
pytest --cov=agents --cov-report=html tests/
```

### Validate Your Installation

```python
# Test script
import asyncio
from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator

async def test_setup():
    """Test your swarm setup."""
    try:
        swarm = PydanticAISwarmOrchestrator("TestSwarm")
        await swarm.start_swarm()

        # Test basic functionality
        status = await swarm.get_swarm_status()
        assert status['is_active'] == True

        await swarm.stop_swarm()
        print("✅ Setup validation passed!")

    except Exception as e:
        print(f"❌ Setup validation failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_setup())
```

## 🚨 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### OpenAI API errors
```bash
# Check your API key
echo $OPENAI_API_KEY

# Test API connectivity
python -c "import openai; print('API key valid')"
```

#### Swarm startup failures
```python
# Check swarm status
status = await swarm.get_swarm_status()
print(f"Swarm active: {status['is_active']}")

# Check agent health
for agent_name in swarm.agents:
    agent_status = await swarm.agents[agent_name].get_status_async()
    print(f"{agent_name}: {agent_status['is_active']}")
```

### Getting Help

- **Documentation**: [Complete Documentation](../PYDANTIC_AI_SWARM_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/your-org/pydantic-ai-swarm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/pydantic-ai-swarm/discussions)

## 🎯 Next Steps

Now that you have a working swarm, explore:

1. **[Agent Development](agent-development.md)** - Create custom agents
2. **[Tool System](tool-system.md)** - Build and integrate tools
3. **[Swarm Orchestration](swarm-orchestration.md)** - Advanced swarm management
4. **[Production Deployment](production-deployment.md)** - Scale to production

## 📚 Additional Resources

- **API Reference**: Complete API documentation
- **Examples**: Working code examples
- **Best Practices**: Performance and security guidelines
- **Architecture Guide**: System design and patterns

---

**Congratulations!** You've successfully set up your first Pydantic AI Democratic Agent Swarm. Ready to build autonomous AI systems? Continue with the [Agent Development Guide](agent-development.md)!
