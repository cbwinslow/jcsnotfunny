# Agent Development Guide

This guide explains how to create, configure, and deploy custom agents for the Pydantic AI Democratic Agent Swarm system.

## 🏗️ Agent Architecture

### Base Agent Classes

All agents inherit from the `PydanticAIAgent` base class:

```python
from agents.pydantic_ai_agent import PydanticAIAgent
from agents.models.agent_config import AgentConfig

class CustomAgent(PydanticAIAgent):
    """Custom agent implementation."""

    def __init__(self, agent_name: str, **kwargs):
        super().__init__(agent_name, **kwargs)
        # Custom initialization
```

### Agent Lifecycle

Agents follow a defined lifecycle:

1. **Initialization**: Configuration and setup
2. **Registration**: Added to swarm orchestrator
3. **Activation**: Started and ready for tasks
4. **Execution**: Processing tasks democratically
5. **Deactivation**: Graceful shutdown

## 🛠️ Creating Custom Agents

### Basic Agent Template

```python
from typing import Any, Dict, List, Optional
from agents.pydantic_ai_agent import PydanticAIAgent
from agents.models.agent_config import AgentConfig
from agents.models.results import ToolResult

class ContentAnalysisAgent(PydanticAIAgent):
    """Agent specialized in content analysis and optimization."""

    def __init__(self, agent_name: str, **kwargs):
        super().__init__(agent_name, **kwargs)

        # Set default configuration if not provided
        if not hasattr(self, 'config') or self.config is None:
            self.config = self._create_default_config()

    def _create_default_config(self) -> AgentConfig:
        """Create default agent configuration."""
        return AgentConfig(
            name=self.agent_name,
            role="Content Analysis Specialist",
            model="gpt-4o",
            system_prompt="""You are a content analysis specialist.
            Your expertise includes content quality assessment, audience analysis,
            engagement prediction, and optimization recommendations.

            Always provide detailed, actionable insights with confidence scores.""",
            domain_expertise=[
                "content_analysis",
                "audience_engagement",
                "optimization",
                "quality_assessment"
            ],
            tools=[
                {
                    "name": "analyze_content",
                    "description": "Analyze content for quality and engagement",
                    "inputSchema": {
                        "type": "object",
                        "required": ["content"],
                        "properties": {
                            "content": {"type": "string", "description": "Content to analyze"},
                            "analysis_type": {
                                "type": "string",
                                "enum": ["comprehensive", "engagement", "quality"],
                                "default": "comprehensive"
                            },
                            "target_audience": {"type": "string", "description": "Target audience description"}
                        }
                    }
                },
                {
                    "name": "optimize_content",
                    "description": "Provide optimization recommendations",
                    "inputSchema": {
                        "type": "object",
                        "required": ["content", "current_metrics"],
                        "properties": {
                            "content": {"type": "string"},
                            "current_metrics": {"type": "object"},
                            "platform": {"type": "string", "enum": ["twitter", "instagram", "tiktok", "youtube"]}
                        }
                    }
                }
            ],
            max_concurrent_tasks=3,
            voting_enabled=True,
            confidence_thresholds={
                "voting": 0.4,
                "communication": 0.5,
                "execution": 0.6
            }
        )

    async def _execute_tool_core(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute tool logic."""
        if tool_name == "analyze_content":
            return await self._analyze_content(parameters)
        elif tool_name == "optimize_content":
            return await self._optimize_content(parameters)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def _analyze_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content for quality and engagement."""
        content = parameters["content"]
        analysis_type = parameters.get("analysis_type", "comprehensive")
        target_audience = parameters.get("target_audience", "general")

        # Implement content analysis logic
        analysis = {
            "content_length": len(content),
            "readability_score": self._calculate_readability(content),
            "engagement_potential": self._assess_engagement_potential(content, target_audience),
            "sentiment": self._analyze_sentiment(content),
            "topics": self._extract_topics(content),
            "recommendations": self._generate_recommendations(content, analysis_type)
        }

        return analysis

    async def _optimize_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Provide content optimization recommendations."""
        content = parameters["content"]
        current_metrics = parameters["current_metrics"]
        platform = parameters.get("platform", "general")

        # Generate optimization suggestions
        optimization = {
            "current_performance": current_metrics,
            "suggested_improvements": self._generate_improvements(content, current_metrics, platform),
            "platform_specific_tips": self._get_platform_tips(platform),
            "predicted_impact": self._estimate_impact(current_metrics),
            "implementation_priority": "high"  # high, medium, low
        }

        return optimization

    # Helper methods
    def _calculate_readability(self, content: str) -> float:
        """Calculate content readability score."""
        # Simplified readability calculation
        words = len(content.split())
        sentences = len([s for s in content.split('.') if s.strip()])
        avg_words_per_sentence = words / max(sentences, 1)

        # Flesch Reading Ease score (simplified)
        score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * (len(content) / max(words, 1)))
        return max(0.0, min(100.0, score))

    def _assess_engagement_potential(self, content: str, audience: str) -> float:
        """Assess content's engagement potential."""
        # Simplified engagement assessment
        score = 0.5  # Base score

        # Factors that increase engagement
        if any(word in content.lower() for word in ["question", "ask", "what", "how", "why"]):
            score += 0.1
        if "!" in content or "?" in content:
            score += 0.1
        if len(content) < 280:  # Twitter-length content
            score += 0.1

        return min(1.0, score)

    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze content sentiment."""
        return {
            "polarity": 0.2,  # -1 to 1
            "subjectivity": 0.4,  # 0 to 1
            "label": "positive"
        }

    def _extract_topics(self, content: str) -> List[str]:
        """Extract main topics from content."""
        # Simplified topic extraction
        return ["content_creation", "engagement", "optimization"]

    def _generate_recommendations(self, content: str, analysis_type: str) -> List[str]:
        """Generate content recommendations."""
        recommendations = []

        if len(content) > 500:
            recommendations.append("Consider breaking long content into shorter, digestible pieces")
        if not any(char in content for char in ["!", "?"]):
            recommendations.append("Add questions or exclamations to increase engagement")
        if analysis_type == "engagement":
            recommendations.append("Include a clear call-to-action to boost interaction")

        return recommendations

    def _generate_improvements(self, content: str, metrics: Dict[str, Any], platform: str) -> List[Dict[str, Any]]:
        """Generate specific improvement suggestions."""
        improvements = []

        if platform == "twitter":
            improvements.append({
                "type": "hashtag_optimization",
                "description": "Add relevant hashtags to increase visibility",
                "impact": "medium",
                "effort": "low"
            })

        if metrics.get("engagement_rate", 0) < 0.05:
            improvements.append({
                "type": "hook_improvement",
                "description": "Strengthen the opening hook to capture attention faster",
                "impact": "high",
                "effort": "medium"
            })

        return improvements

    def _get_platform_tips(self, platform: str) -> List[str]:
        """Get platform-specific optimization tips."""
        tips = {
            "twitter": [
                "Use 1-2 relevant hashtags",
                "Keep under 280 characters for full visibility",
                "Include a question to encourage replies"
            ],
            "instagram": [
                "Use relevant emojis in captions",
                "Include a call-to-action in the first line",
                "Use location tags when relevant"
            ],
            "tiktok": [
                "Hook viewers in the first 3 seconds",
                "Use trending sounds and effects",
                "Include text overlays for accessibility"
            ]
        }

        return tips.get(platform, ["Optimize content for the target platform"])

    def _estimate_impact(self, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate impact of optimizations."""
        return {
            "engagement_increase": 0.15,  # 15% increase
            "reach_improvement": 0.10,    # 10% improvement
            "confidence": 0.75
        }
```

### Advanced Agent Features

#### Custom Confidence Logic

```python
class AdvancedContentAgent(ContentAnalysisAgent):
    """Agent with advanced confidence calculation."""

    async def calculate_task_confidence(self, task_description: str, context: Dict[str, Any]) -> float:
        """Calculate confidence for specific tasks."""
        domain = context.get("domain", "")

        # Base confidence from domain expertise
        base_confidence = self.confidence.get_domain_confidence(domain)

        # Adjust based on task complexity
        if "comprehensive" in task_description.lower():
            base_confidence *= 0.9  # Slightly reduce for complex tasks
        elif "quick" in task_description.lower():
            base_confidence *= 1.1  # Increase for simple tasks

        # Adjust based on available tools
        tool_match = any(tool["name"] in task_description.lower()
                        for tool in self.config.tools)
        if tool_match:
            base_confidence *= 1.2

        return min(1.0, base_confidence)

    async def should_abstain_from_vote(self, context: str = "", threshold: float = 0.3) -> bool:
        """Custom abstention logic."""
        # Always participate in content-related decisions
        if "content" in context.lower():
            return False

        # Use standard logic for other domains
        return await super().should_abstain_from_vote(context, threshold)
```

#### Inter-Agent Communication

```python
class CollaborativeAgent(PydanticAIAgent):
    """Agent that collaborates with other agents."""

    async def request_collaboration(self, task: str, collaborators: List[str]) -> Dict[str, Any]:
        """Request collaboration from other agents."""
        collaboration_request = {
            "task": task,
            "requester": self.agent_name,
            "collaborators": collaborators,
            "deadline": time.time() + 300  # 5 minutes
        }

        # Send collaboration request via swarm communication
        await self._send_message(
            MessageType.COLLABORATION_REQUEST,
            collaboration_request,
            recipients=collaborators
        )

        # Wait for responses
        responses = await self._collect_responses(collaborators, timeout=300)

        return self._consolidate_responses(responses)

    async def handle_collaboration_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming collaboration request."""
        task = request["task"]

        # Assess if we can contribute
        confidence = await self.calculate_task_confidence(task, {})

        if confidence > 0.6:
            # Provide contribution
            contribution = await self._generate_contribution(task)
            return {
                "agent": self.agent_name,
                "participating": True,
                "confidence": confidence,
                "contribution": contribution
            }
        else:
            return {
                "agent": self.agent_name,
                "participating": False,
                "reason": "Low confidence in task"
            }
```

## ⚙️ Agent Configuration

### Configuration Options

```python
agent_config = AgentConfig(
    # Basic information
    name="content_analyzer_v2",
    role="Senior Content Analysis Specialist",
    model="gpt-4o",

    # System prompt
    system_prompt="""You are an expert content analyst with 10+ years experience.
    Provide detailed, data-driven insights with actionable recommendations.""",

    # Domain expertise
    domain_expertise=[
        "content_analysis",
        "engagement_optimization",
        "audience_behavior",
        "platform_analytics",
        "trend_analysis"
    ],

    # Tool definitions
    tools=[
        {
            "name": "comprehensive_analysis",
            "description": "Full content analysis suite",
            "inputSchema": {
                "type": "object",
                "required": ["content"],
                "properties": {
                    "content": {"type": "string"},
                    "platforms": {"type": "array", "items": {"type": "string"}},
                    "include_competitor_analysis": {"type": "boolean", "default": False}
                }
            }
        }
    ],

    # Performance settings
    max_concurrent_tasks=5,
    timeout_seconds=600,

    # Democratic participation
    voting_enabled=True,
    confidence_thresholds={
        "voting": 0.5,      # Higher threshold for voting
        "communication": 0.4,
        "execution": 0.7    # High threshold for task execution
    },

    # Advanced features
    telemetry_enabled=True,
    health_check_interval=30,
    enable_performance_tracking=True
)
```

### Environment-Based Configuration

```python
import os
from agents.models.agent_config import AgentConfig

def create_agent_from_env() -> ContentAnalysisAgent:
    """Create agent with environment-based configuration."""

    # Get configuration from environment
    agent_name = os.getenv("AGENT_NAME", "content_agent")
    model = os.getenv("AGENT_MODEL", "gpt-4o")
    max_tasks = int(os.getenv("AGENT_MAX_TASKS", "3"))

    # Domain expertise from comma-separated list
    domain_expertise = os.getenv("AGENT_DOMAINS", "content_analysis,engagement").split(",")

    config = AgentConfig(
        name=agent_name,
        role="Content Analysis Agent",
        model=model,
        domain_expertise=[d.strip() for d in domain_expertise],
        max_concurrent_tasks=max_tasks,
        voting_enabled=os.getenv("AGENT_VOTING_ENABLED", "true").lower() == "true"
    )

    return ContentAnalysisAgent(agent_name, config=config)
```

## 🧪 Testing Agents

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestContentAnalysisAgent:

    @pytest.fixture
    async def agent(self):
        """Create test agent."""
        agent = ContentAnalysisAgent("test_agent")
        yield agent

    @pytest.mark.asyncio
    async def test_content_analysis(self, agent):
        """Test content analysis functionality."""
        test_content = "This is a sample article about AI technology and automation."

        with patch.object(agent, 'ai_agent') as mock_ai:
            mock_ai.run.return_value = AsyncMock(data={"analysis": "mock_result"})

            result = await agent._analyze_content({"content": test_content})

            assert "content_length" in result
            assert result["content_length"] == len(test_content)
            assert "engagement_potential" in result

    @pytest.mark.asyncio
    async def test_agent_voting(self, agent):
        """Test agent voting behavior."""
        # Test confident voting
        vote = await agent.cast_vote("Content optimization proposal", "content_analysis")

        assert "decision" in vote
        assert "weight" in vote
        assert isinstance(vote["weight"], float)

    @pytest.mark.asyncio
    async def test_low_confidence_abstention(self, agent):
        """Test abstention with low confidence."""
        # Force low confidence
        agent.confidence.overall = 0.2

        should_abstain = agent.should_abstain_from_vote("unknown_domain")
        assert should_abstain is True
```

### Integration Tests

```python
class TestAgentIntegration:

    @pytest.mark.asyncio
    async def test_agent_swarm_integration(self):
        """Test agent integration with swarm."""
        from agents.pydantic_ai_swarm_orchestrator import PydanticAISwarmOrchestrator

        # Create swarm and agent
        swarm = PydanticAISwarmOrchestrator("test_swarm")
        agent = ContentAnalysisAgent("content_agent")

        # Register and start
        await swarm.register_agent(agent)
        await swarm.start_swarm()

        # Execute task
        result = await swarm.execute_task(
            "Analyze this content for engagement",
            {"domain": "content_analysis", "content": "Sample content"}
        )

        assert result.success is True
        assert "analysis" in result.data

        # Cleanup
        await swarm.stop_swarm()

    @pytest.mark.asyncio
    async def test_agent_tool_integration(self):
        """Test agent tool integration."""
        from agents.tools import tool_factory

        agent = ContentAnalysisAgent("tool_test_agent")

        # Register agent tools
        for tool in agent.config.tools:
            await tool_factory.register_tool_with_registry(
                agent,  # This would need proper tool implementation
                agent.agent_name
            )

        # Verify tools are registered
        registry = tool_factory.get_registry()
        tools = registry.list_tools(agent_name=agent.agent_name)

        assert len(tools) > 0
```

## 📊 Agent Monitoring

### Health Monitoring

```python
agent = ContentAnalysisAgent("monitored_agent")

# Get agent status
status = await agent.get_status_async()

print("Agent Status:")
print(f"Active: {status['is_active']}")
print(f"Confidence: {status['confidence']['overall']:.2f}")
print(f"Tasks Processed: {status['tasks_processed']}")
print(f"Success Rate: {status['success_rate']:.2f}")

# Monitor performance
if hasattr(agent, 'performance_metrics'):
    metrics = agent.performance_metrics
    print(f"Average Response Time: {metrics['avg_response_time']:.2f}s")
    print(f"Error Rate: {metrics['error_rate']:.2f}")
```

### Custom Metrics

```python
class MetricsEnabledAgent(ContentAnalysisAgent):
    """Agent with custom performance metrics."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_metrics = {
            "analyses_performed": 0,
            "average_analysis_time": 0.0,
            "content_types_processed": set()
        }

    async def _analyze_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Override to add custom metrics."""
        start_time = time.time()

        # Perform analysis
        result = await super()._analyze_content(parameters)

        # Update metrics
        analysis_time = time.time() - start_time
        self.custom_metrics["analyses_performed"] += 1
        self.custom_metrics["average_analysis_time"] = (
            (self.custom_metrics["average_analysis_time"] *
             (self.custom_metrics["analyses_performed"] - 1) +
             analysis_time) / self.custom_metrics["analyses_performed"]
        )

        content_type = parameters.get("analysis_type", "general")
        self.custom_metrics["content_types_processed"].add(content_type)

        return result

    def get_custom_metrics(self) -> Dict[str, Any]:
        """Get custom performance metrics."""
        return {
            **self.custom_metrics,
            "content_types_count": len(self.custom_metrics["content_types_processed"])
        }
```

## 🚀 Production Deployment

### Agent Scaling

```python
# Scale agent based on load
class ScalableContentAgent(ContentAnalysisAgent):
    """Agent that can scale based on demand."""

    def __init__(self, *args, max_instances: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_instances = max_instances
        self.instances = [self]  # Start with self

    async def scale_up(self, demand_level: float) -> None:
        """Scale up based on demand."""
        if demand_level > 0.8 and len(self.instances) < self.max_instances:
            # Create additional instances
            new_instance = ScalableContentAgent(
                f"{self.agent_name}_instance_{len(self.instances)}"
            )
            self.instances.append(new_instance)

            # Register with swarm (assuming swarm reference)
            if hasattr(self, 'swarm'):
                await self.swarm.register_agent(new_instance)

    async def scale_down(self, demand_level: float) -> None:
        """Scale down when demand is low."""
        if demand_level < 0.3 and len(self.instances) > 1:
            # Remove excess instances
            instance_to_remove = self.instances.pop()

            if hasattr(self, 'swarm'):
                await self.swarm.unregister_agent(instance_to_remove.agent_name)
```

### Agent Updates

```python
class SelfUpdatingAgent(ContentAnalysisAgent):
    """Agent that can update its own capabilities."""

    async def check_for_updates(self) -> Dict[str, Any]:
        """Check for available updates."""
        # In a real implementation, this would check a central registry
        # or configuration service for updates

        return {
            "available_updates": [],
            "current_version": "1.0.0",
            "latest_version": "1.1.0"
        }

    async def apply_update(self, update_info: Dict[str, Any]) -> bool:
        """Apply agent updates."""
        try:
            # Backup current state
            backup = self._create_backup()

            # Apply update logic
            if update_info.get("type") == "model_update":
                self.config.model = update_info["new_model"]
            elif update_info.get("type") == "tool_update":
                await self._update_tools(update_info["new_tools"])

            # Validate update
            await self._validate_update()

            self.logger.info(f"Successfully updated agent: {update_info}")
            return True

        except Exception as e:
            # Rollback on failure
            await self._restore_backup(backup)
            self.logger.error(f"Update failed, rolled back: {e}")
            return False

    def _create_backup(self) -> Dict[str, Any]:
        """Create backup of current state."""
        return {
            "config": self.config.dict(),
            "confidence": self.confidence.__dict__,
            "timestamp": time.time()
        }

    async def _restore_backup(self, backup: Dict[str, Any]) -> None:
        """Restore from backup."""
        self.config = AgentConfig(**backup["config"])
        # Restore other state...
```

## 📚 Best Practices

### Agent Design

1. **Single Responsibility**: Each agent should have one primary function
2. **Clear Interfaces**: Well-defined inputs and outputs
3. **Error Handling**: Comprehensive error handling and recovery
4. **Monitoring**: Built-in health and performance monitoring
5. **Documentation**: Clear docstrings and usage examples

### Performance Optimization

1. **Caching**: Implement intelligent result caching
2. **Async Operations**: Use async/await for I/O operations
3. **Resource Limits**: Set appropriate timeouts and limits
4. **Metrics Collection**: Track performance metrics
5. **Scalability**: Design for horizontal scaling

### Security Considerations

1. **Input Validation**: Validate all inputs thoroughly
2. **Output Sanitization**: Sanitize outputs before returning
3. **Access Control**: Implement proper authorization
4. **Audit Logging**: Log all significant operations
5. **Secure Communication**: Use encrypted channels

### Testing Strategy

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **Performance Tests**: Validate under load
4. **Chaos Testing**: Test failure scenarios
5. **Continuous Testing**: Automated testing in CI/CD

## 🎯 Advanced Patterns

### Agent Composition

```python
class CompositeAnalysisAgent(PydanticAIAgent):
    """Agent composed of multiple specialized sub-agents."""

    def __init__(self, agent_name: str, **kwargs):
        super().__init__(agent_name, **kwargs)

        # Initialize sub-agents
        self.quality_agent = ContentQualityAgent("quality_subagent")
        self.engagement_agent = EngagementAnalysisAgent("engagement_subagent")
        self.optimization_agent = ContentOptimizationAgent("optimization_subagent")

        # Composition strategy
        self.composition_strategy = "parallel"  # parallel, sequential, or hierarchical

    async def _execute_composite_analysis(self, content: str) -> Dict[str, Any]:
        """Execute analysis using sub-agents."""
        if self.composition_strategy == "parallel":
            # Run all analyses in parallel
            tasks = [
                self.quality_agent.analyze_quality(content),
                self.engagement_agent.analyze_engagement(content),
                self.optimization_agent.generate_optimizations(content)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine results
            return self._merge_parallel_results(results)

        elif self.composition_strategy == "sequential":
            # Run analyses sequentially, each building on previous
            quality_result = await self.quality_agent.analyze_quality(content)
            engagement_result = await self.engagement_agent.analyze_engagement(content, quality_result)
            optimization_result = await self.optimization_agent.generate_optimizations(content, engagement_result)

            return self._merge_sequential_results(quality_result, engagement_result, optimization_result)
```

### Meta-Agent Pattern

```python
class MetaAgent(PydanticAIAgent):
    """Agent that creates and manages other agents."""

    async def create_specialized_agent(self, task_description: str) -> PydanticAIAgent:
        """Dynamically create a specialized agent for a task."""
        # Analyze task requirements
        requirements = await self._analyze_task_requirements(task_description)

        # Generate agent configuration
        config = await self._generate_agent_config(requirements)

        # Create agent class dynamically
        agent_class = await self._create_agent_class(config)

        # Instantiate and configure
        agent_instance = agent_class(f"dynamic_agent_{hash(task_description)}")
        agent_instance.config = config

        return agent_instance

    async def orchestrate_dynamic_team(self, complex_task: str) -> Dict[str, Any]:
        """Create a dynamic team of agents for complex tasks."""
        # Break down complex task
        subtasks = await self._decompose_task(complex_task)

        # Create agents for each subtask
        agents = []
        for subtask in subtasks:
            agent = await self.create_specialized_agent(subtask)
            agents.append(agent)

        # Orchestrate execution
        results = await self._coordinate_team_execution(agents, subtasks)

        # Synthesize final result
        return await self._synthesize_team_results(results)
```

---

## 📞 Support

Need help developing custom agents?

- **Documentation**: [Complete API Reference](../api/agents.md)
- **Examples**: [Agent Examples Repository](../../examples/agents/)
- **Community**: [GitHub Discussions](https://github.com/your-org/pydantic-ai-swarm/discussions)
- **Enterprise**: Contact enterprise@pydantic-ai-swarm.com

## 🎯 Next Steps

Now that you understand agent development:

1. **[Swarm Orchestration](swarm-orchestration.md)** - Learn about swarm management
2. **[Tool Development](tool-system.md)** - Create custom tools
3. **[Production Deployment](production-deployment.md)** - Deploy at scale
4. **[API Reference](../api/)** - Complete API documentation

**Happy agent development! 🤖✨**
