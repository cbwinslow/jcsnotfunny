"""Base Agent Classes - Foundation for all production agents.

This module provides the base classes for implementing agents that can:
- Consume configuration from agents_config.json
- Execute tools using the RobustTool framework
- Participate in workflows and agent communication
- Maintain state and provide monitoring capabilities
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path

from agents.robust_tool import RobustTool, ToolResult


class AgentTool:
    """Wrapper for agent tools that integrates with RobustTool framework."""

    def __init__(self, name: str, description: str, config: Optional[Dict[str, Any]] = None):
        """Initialize agent tool.

        Args:
            name: Tool name
            description: Tool description
            config: Optional tool configuration
        """
        self.name = name
        self.description = description
        self.config = config or {}

        # Create the actual RobustTool implementation
        self.implementation = self._create_implementation()

    @abstractmethod
    def _create_implementation(self) -> RobustTool:
        """Create the RobustTool implementation for this agent tool.

        Returns:
            Configured RobustTool instance
        """
        pass

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        """Execute the tool with given parameters.

        Args:
            parameters: Tool parameters

        Returns:
            ToolResult with execution outcome
        """
        return self.implementation.execute(parameters)

    def get_stats(self) -> Dict[str, Any]:
        """Get tool execution statistics.

        Returns:
            Dictionary with tool statistics
        """
        return self.implementation.get_stats()


class BaseAgent(ABC):
    """Base class for all production agents.

    Provides common functionality for:
    - Configuration loading from agents_config.json
    - Tool management and execution
    - State management and monitoring
    - Workflow participation
    """

    def __init__(self, agent_name: str, config_path: Optional[str] = None):
        """Initialize the agent.

        Args:
            agent_name: Name of the agent (must match agents_config.json)
            config_path: Optional path to agents_config.json
        """
        self.agent_name = agent_name
        self.config_path = config_path or "agents_config.json"

        # Setup logging
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{agent_name}")
        self.logger.setLevel(logging.INFO)

        # Load configuration
        self.config = self._load_config()
        self.agent_config = self.config.get("agents", {}).get(agent_name, {})

        if not self.agent_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")

        # Initialize components
        self.name = self.agent_config.get("name", agent_name)
        self.role = self.agent_config.get("role", "")
        self.model = self.agent_config.get("model", "gpt-4o")
        self.system_prompt = self.agent_config.get("system_prompt", "")
        self.workflow_configs = self.agent_config.get("workflows", {})

        # Initialize tools
        self.tools = self._initialize_tools()

        # State management
        self.state = {}
        self.execution_history: List[Dict[str, Any]] = []

        self.logger.info(f"Initialized agent '{self.name}' with {len(self.tools)} tools")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from agents_config.json.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(config_file, 'r') as f:
            return json.load(f)

    @abstractmethod
    def _initialize_tools(self) -> Dict[str, AgentTool]:
        """Initialize agent-specific tools.

        Returns:
            Dictionary mapping tool names to AgentTool instances
        """
        pass

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a specific tool.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters

        Returns:
            ToolResult with execution outcome

        Raises:
            ValueError: If tool doesn't exist
        """
        if tool_name not in self.tools:
            available_tools = list(self.tools.keys())
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available_tools}")

        self.logger.info(f"Executing tool '{tool_name}' with parameters: {parameters}")

        result = self.tools[tool_name].execute(parameters)

        # Record execution in history
        execution_record = {
            'timestamp': result.execution_id.split('_')[1],  # Extract timestamp from ID
            'tool': tool_name,
            'parameters': parameters,
            'result': result.to_dict(),
            'success': result.success
        }
        self.execution_history.append(execution_record)

        if result.success:
            self.logger.info(f"Tool '{tool_name}' executed successfully")
        else:
            self.logger.error(f"Tool '{tool_name}' failed: {result.error}")

        return result

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool information dictionary or None if not found
        """
        if tool_name not in self.tools:
            return None

        tool = self.tools[tool_name]
        return {
            'name': tool.name,
            'description': tool.description,
            'stats': tool.get_stats()
        }

    def execute_workflow(self, workflow_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a predefined workflow.

        Args:
            workflow_name: Name of the workflow to execute
            inputs: Input parameters for the workflow

        Returns:
            Dictionary with workflow execution results

        Raises:
            ValueError: If workflow doesn't exist
        """
        if workflow_name not in self.workflow_configs:
            available_workflows = list(self.workflow_configs.keys())
            raise ValueError(f"Workflow '{workflow_name}' not found. Available workflows: {available_workflows}")

        workflow_config = self.workflow_configs[workflow_name]
        self.logger.info(f"Executing workflow '{workflow_name}' with inputs: {inputs}")

        results = {}
        current_inputs = inputs.copy()

        # Execute workflow steps (simplified - assumes sequential execution)
        for step in workflow_config:
            step_name = step.get('name', f"{step['agent']}.{step['action']}")
            tool_name = step['action']
            step_inputs = self._prepare_step_inputs(step, current_inputs, results)

            self.logger.debug(f"Executing workflow step: {step_name}")
            step_result = self.execute_tool(tool_name, step_inputs)

            results[step_name] = step_result

            if not step_result.success:
                self.logger.error(f"Workflow '{workflow_name}' failed at step '{step_name}': {step_result.error}")
                break

        workflow_result = {
            'workflow': workflow_name,
            'success': all(r.success for r in results.values()),
            'results': {k: v.to_dict() for k, v in results.items()},
            'inputs': inputs
        }

        self.logger.info(f"Workflow '{workflow_name}' completed with success: {workflow_result['success']}")
        return workflow_result

    def _prepare_step_inputs(self, step: Dict[str, Any], workflow_inputs: Dict[str, Any],
                           previous_results: Dict[str, ToolResult]) -> Dict[str, Any]:
        """Prepare inputs for a workflow step.

        Args:
            step: Step configuration
            workflow_inputs: Original workflow inputs
            previous_results: Results from previous steps

        Returns:
            Prepared inputs for the step
        """
        # This is a simplified implementation
        # In practice, you'd want more sophisticated input mapping
        step_inputs = {}

        # Map step inputs from workflow inputs and previous results
        input_mapping = step.get('input', {})
        if isinstance(input_mapping, str):
            # Simple string mapping - could be enhanced
            if input_mapping in workflow_inputs:
                step_inputs = workflow_inputs[input_mapping]
            elif input_mapping in previous_results:
                step_inputs = previous_results[input_mapping].data
            else:
                step_inputs = workflow_inputs  # Fallback to all inputs
        elif isinstance(input_mapping, dict):
            # Dict mapping - more complex logic would go here
            step_inputs = workflow_inputs
        else:
            step_inputs = workflow_inputs

        return step_inputs

    def get_status(self) -> Dict[str, Any]:
        """Get agent status and statistics.

        Returns:
            Dictionary with agent status information
        """
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for r in self.execution_history if r['success'])
        success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0

        tool_stats = {}
        for tool_name, tool in self.tools.items():
            tool_stats[tool_name] = tool.get_stats()

        return {
            'name': self.name,
            'role': self.role,
            'model': self.model,
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'success_rate': success_rate,
            'available_tools': self.get_available_tools(),
            'workflows': list(self.workflow_configs.keys()),
            'tool_stats': tool_stats,
            'state': self.state.copy()
        }

    def update_state(self, key: str, value: Any) -> None:
        """Update agent state.

        Args:
            key: State key
            value: State value
        """
        self.state[key] = value
        self.logger.debug(f"Updated state: {key} = {value}")

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get value from agent state.

        Args:
            key: State key
            default: Default value if key doesn't exist

        Returns:
            State value or default
        """
        return self.state.get(key, default)

    def reset_stats(self) -> None:
        """Reset agent execution statistics."""
        self.execution_history.clear()
        for tool in self.tools.values():
            tool.implementation.reset_stats()
        self.logger.info("Reset agent statistics")


class ToolBasedAgent(BaseAgent):
    """Agent that uses RobustTool implementations for its tools.

    This is the most common agent type that automatically creates tools
    from the agent's configuration in agents_config.json.
    """

    def _initialize_tools(self) -> Dict[str, AgentTool]:
        """Initialize tools from agent configuration.

        Returns:
            Dictionary of agent tools
        """
        tools = {}

        # Get tool configurations from agent config
        tool_configs = self.agent_config.get("tools", [])

        for tool_config in tool_configs:
            tool_name = tool_config["name"]
            tool_description = tool_config["description"]
            tool_params_config = tool_config.get("parameters", {})

            # Create agent tool wrapper
            agent_tool = ConfiguredAgentTool(
                name=tool_name,
                description=tool_description,
                config=tool_params_config
            )

            tools[tool_name] = agent_tool

        return tools


class ConfiguredAgentTool(AgentTool):
    """Agent tool that creates RobustTool implementations based on configuration."""

    def _create_implementation(self) -> RobustTool:
        """Create a RobustTool implementation for this configured tool.

        This is a placeholder - actual implementations would be created
        based on the tool type and configuration.

        Returns:
            RobustTool instance (placeholder implementation)
        """
        # This would be replaced with actual tool implementations
        # For now, return a placeholder that raises NotImplementedError
        return PlaceholderRobustTool(self.name, self.description, self.config)


class PlaceholderRobustTool(RobustTool):
    """Placeholder RobustTool for tools that haven't been implemented yet."""

    def _define_fallback_strategies(self) -> List[Dict[str, Any]]:
        """Define basic fallback strategies."""
        return [
            {
                'name': 'log_error',
                'condition': lambda e, p, eid: True,  # Always apply
                'action': lambda e, p, eid: ToolResult(
                    success=False,
                    error=f"Tool '{self.name}' not yet implemented: {str(e)}",
                    execution_id=eid
                ),
                'priority': 1
            }
        ]

    def _define_validation_schema(self) -> Dict[str, Any]:
        """Define basic validation schema."""
        return {
            'type': 'object',
            'properties': {},
            'required': []
        }

    def _execute_core(self, parameters: Dict[str, Any], execution_id: str) -> Any:
        """Core execution - raise NotImplementedError."""
        raise NotImplementedError(f"Tool '{self.name}' has not been implemented yet")


class WorkflowOrchestrator:
    """Orchestrates multi-agent workflows defined in agents_config.json."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize workflow orchestrator.

        Args:
            config_path: Optional path to agents_config.json
        """
        self.config_path = config_path or "agents_config.json"
        self.config = self._load_config()
        self.agents: Dict[str, BaseAgent] = {}

        # Load workflow definitions
        self.workflows = self.config.get("workflows", {})

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from agents_config.json."""
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(config_file, 'r') as f:
            return json.load(f)

    def get_agent(self, agent_name: str) -> BaseAgent:
        """Get or create an agent instance.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent instance

        Raises:
            ValueError: If agent is not configured
        """
        if agent_name not in self.agents:
            # Create agent instance - this would need to be mapped to actual agent classes
            # For now, create a generic ToolBasedAgent
            self.agents[agent_name] = ToolBasedAgent(agent_name, self.config_path)

        return self.agents[agent_name]

    def execute_workflow(self, workflow_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-agent workflow.

        Args:
            workflow_name: Name of the workflow
            inputs: Workflow input parameters

        Returns:
            Workflow execution results

        Raises:
            ValueError: If workflow doesn't exist
        """
        if workflow_name not in self.workflows:
            available_workflows = list(self.workflows.keys())
            raise ValueError(f"Workflow '{workflow_name}' not found. Available workflows: {available_workflows}")

        workflow_config = self.workflows[workflow_name]
        workflow_agents = workflow_config.get("agents", [])
        workflow_steps = workflow_config.get("steps", [])

        logging.info(f"Executing multi-agent workflow '{workflow_name}' with {len(workflow_steps)} steps")

        results = {}
        current_context = inputs.copy()

        # Execute each step
        for step in workflow_steps:
            agent_name = step["agent"]
            action = step["action"]
            step_input = step.get("input", "")

            # Get the agent
            agent = self.get_agent(agent_name)

            # Prepare step inputs (simplified)
            step_parameters = self._resolve_step_inputs(step_input, current_context, results)

            logging.debug(f"Executing step: {agent_name}.{action}")

            # Execute the action
            step_result = agent.execute_tool(action, step_parameters)

            # Store result
            step_key = f"{agent_name}.{action}"
            results[step_key] = step_result

            # Update context for next steps
            if step_result.success:
                current_context[step_key] = step_result.data

            # Stop on failure (could be made configurable)
            if not step_result.success:
                logging.error(f"Workflow '{workflow_name}' failed at step '{step_key}': {step_result.error}")
                break

        workflow_success = all(r.success for r in results.values())

        return {
            'workflow': workflow_name,
            'success': workflow_success,
            'steps_executed': len(results),
            'results': {k: v.to_dict() for k, v in results.items()},
            'inputs': inputs
        }

    def _resolve_step_inputs(self, input_spec: str, context: Dict[str, Any],
                           results: Dict[str, ToolResult]) -> Dict[str, Any]:
        """Resolve step inputs from specification.

        Args:
            input_spec: Input specification string
            context: Current workflow context
            results: Previous step results

        Returns:
            Resolved input parameters
        """
        # This is a simplified implementation
        # In practice, you'd want more sophisticated input resolution

        if not input_spec:
            return context

        # Simple key resolution
        if input_spec in context:
            return context[input_spec]

        # Check results
        if input_spec in results:
            return results[input_spec].data

        # Default to entire context
        return context

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflows.

        Returns:
            List of workflow names
        """
        return list(self.workflows.keys())

    def get_workflow_info(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a workflow.

        Args:
            workflow_name: Name of the workflow

        Returns:
            Workflow information or None if not found
        """
        if workflow_name not in self.workflows:
            return None

        workflow = self.workflows[workflow_name]
        return {
            'name': workflow_name,
            'description': workflow.get('description', ''),
            'agents': workflow.get('agents', []),
            'steps': len(workflow.get('steps', []))
        }
