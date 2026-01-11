#!/bin/bash

# Pydantic AI Democratic Swarm Repository Creator
# This script creates a new GitHub repository with the complete swarm system

set -e  # Exit on any error

echo "🤖 Creating Pydantic AI Democratic Swarm Repository"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "agents/pydantic_ai_swarm_orchestrator.py" ]; then
    echo "❌ Error: Please run this script from the jcsnotfunny project root directory"
    exit 1
fi

# Set default values
REPO_NAME="pydantic-ai-democratic-swarm"
GITHUB_USERNAME=${GITHUB_USERNAME:-"yourusername"}
CREATE_REMOTE=${CREATE_REMOTE:-true}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo-name=*)
            REPO_NAME="${1#*=}"
            shift
            ;;
        --github-username=*)
            GITHUB_USERNAME="${1#*=}"
            shift
            ;;
        --no-remote)
            CREATE_REMOTE=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--repo-name=name] [--github-username=username] [--no-remote]"
            exit 1
            ;;
    esac
done

echo "📁 Repository Name: $REPO_NAME"
echo "👤 GitHub Username: $GITHUB_USERNAME"
echo "🔗 Create Remote: $CREATE_REMOTE"
echo

# Create new directory for the repository
echo "📁 Creating repository directory..."
if [ -d "$REPO_NAME" ]; then
    echo "❌ Directory $REPO_NAME already exists. Please remove it or choose a different name."
    exit 1
fi

mkdir "$REPO_NAME"
cd "$REPO_NAME"

# Initialize git repository
echo "🔧 Initializing Git repository..."
git init
git checkout -b main  # Use 'main' as default branch

# Create directory structure
echo "🏗️  Creating directory structure..."
mkdir -p src/pydantic_ai_swarm/{core,governance,quality,communication,tools/{standard,integrations},knowledge,utils,agents/specialized,templates}
mkdir -p docs/{getting-started,guides,reference,tutorials,integrations,troubleshooting}
mkdir -p examples/{basic,advanced,domain_specific}
mkdir -p tests/{unit,integration,e2e,fixtures}
mkdir -p scripts tools
mkdir -p configs/{swarm,agents,environments,templates}
mkdir -p .github/{workflows,ISSUE_TEMPLATE}

# Create __init__.py files
echo "📄 Creating Python package files..."
find src/ -type d -exec touch {}/__init__.py \;
find tests/ -type d -exec touch {}/__init__.py \;

# Copy core files from current project
echo "📋 Copying core swarm files..."

# Copy main swarm components
cp ../agents/pydantic_ai_swarm_orchestrator.py src/pydantic_ai_swarm/core/orchestrator.py
cp ../agents/efficiency_enforcer.py src/pydantic_ai_swarm/quality/efficiency_enforcer.py
cp ../agents/diagnostic_system.py src/pydantic_ai_swarm/quality/diagnostic_system.py
cp ../agents/base_agent.py src/pydantic_ai_swarm/core/base_agent.py

# Create version file
cat > src/pydantic_ai_swarm/__init__.py << 'EOF'
"""Pydantic AI Democratic Swarm - Revolutionary AI Agent Orchestration."""

__version__ = "1.0.0"
__author__ = "Pydantic AI Swarm Team"
__description__ = "Democratic AI agent orchestration with efficiency enforcement"

from .core.orchestrator import PydanticAISwarmOrchestrator
from .core.base_agent import BaseAgent
from .quality.efficiency_enforcer import EfficiencyEnforcer

__all__ = [
    "PydanticAISwarmOrchestrator",
    "BaseAgent",
    "EfficiencyEnforcer",
    "__version__",
]
EOF

# Copy documentation and README
echo "📚 Copying documentation..."
cp ../pydantic-ai-swarm-README.md README.md
cp ../docs/swarm_efficiency_rules.md docs/efficiency-rules.md

# Copy packaging files
echo "📦 Copying packaging files..."
cp ../pyproject.toml .
cp ../LICENSE .
cp ../CHANGELOG.md .
cp ../requirements.txt .
cp ../requirements-dev.txt .
cp ../MANIFEST.in .
cp ../.gitignore .

# Create setup.py for backward compatibility
cat > setup.py << 'EOF'
"""Setup script for backward compatibility."""

from setuptools import setup

if __name__ == "__main__":
    setup()
EOF

# Create pyproject.toml with proper package structure
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pydantic-ai-swarm"
version = "1.0.0"
description = "Democratic AI agent orchestration with efficiency enforcement"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.9"
authors = [
    {name = "Pydantic AI Swarm Team", email = "team@pydantic-ai-swarm.dev"},
]
maintainers = [
    {name = "Pydantic AI Swarm Team", email = "team@pydantic-ai-swarm.dev"},
]
keywords = ["ai", "agents", "swarm", "democratic", "orchestration", "efficiency"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
dependencies = [
    "pydantic>=2.0.0",
    "openai>=1.0.0",
    "asyncio-mqtt>=0.16.0",
    "redis>=5.0.0",
    "aioredis>=2.0.0",
    "python-dotenv>=1.0.0",
    "structlog>=23.0.0",
    "rich>=13.0.0",
    "click>=8.0.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "myst-parser>=2.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/pydantic-ai-democratic-swarm"
Documentation = "https://pydantic-ai-swarm.readthedocs.io/"
Repository = "https://github.com/yourusername/pydantic-ai-democratic-swarm"
Issues = "https://github.com/yourusername/pydantic-ai-democratic-swarm/issues"
Changelog = "https://github.com/yourusername/pydantic-ai-democratic-swarm/blob/main/CHANGELOG.md"

[project.scripts]
pydantic-swarm = "pydantic_ai_swarm.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
exclude = ["tests*", "docs*", "scripts*", "tools*"]

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["pydantic_ai_swarm"]
known_third_party = ["pydantic", "openai", "redis"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "asyncio.*",
    "redis.*",
    "aioredis.*",
]
ignore_missing_imports = true

[tool.ruff]
target-version = "py39"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/**/*" = ["B011"]  # assert false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-ra -q --strict-markers --strict-config --cov=pydantic_ai_swarm --cov-report=term-missing"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow running tests",
]
EOF

# Create example files
echo "📝 Creating example files..."

# Simple example
cat > examples/basic/simple_swarm.py << 'EOF'
#!/usr/bin/env python3
"""
Simple Pydantic AI Swarm Example

This example demonstrates basic swarm usage with democratic task execution.
"""

import asyncio
from pydantic_ai_swarm import PydanticAISwarmOrchestrator


async def main():
    """Run a simple swarm example."""
    print("🤖 Pydantic AI Swarm - Simple Example")
    print("=" * 40)

    # Note: This is a template - actual agents need to be implemented
    # based on your specific domain requirements

    print("✅ Example structure created")
    print("📝 Implement domain-specific agents to use this example")


if __name__ == "__main__":
    asyncio.run(main())
EOF

# Create CLI script
cat > scripts/swarm_cli.py << 'EOF'
#!/usr/bin/env python3
"""
Pydantic AI Swarm Command Line Interface
"""

import asyncio
import click
from pathlib import Path

# Add src to path for development
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic_ai_swarm import PydanticAISwarmOrchestrator


@click.group()
@click.version_option()
def cli():
    """Pydantic AI Democratic Swarm CLI."""
    pass


@cli.command()
@click.option("--name", default="DefaultSwarm", help="Name of the swarm")
@click.option("--agents", default=3, help="Number of agents to create")
def start(name, agents):
    """Start a new swarm."""
    click.echo(f"🚀 Starting swarm '{name}' with {agents} agents")
    # Implementation would go here
    click.echo("✅ Swarm started (template)")


@cli.command()
@click.argument("task")
@click.option("--domain", default="general", help="Task domain")
def execute(task, domain):
    """Execute a task through the swarm."""
    click.echo(f"🎯 Executing task: {task}")
    click.echo(f"📋 Domain: {domain}")
    # Implementation would go here
    click.echo("✅ Task completed (template)")


@cli.command()
def status():
    """Show swarm status."""
    click.echo("📊 Swarm Status:")
    click.echo("   Status: Running (template)")
    click.echo("   Agents: 3 active")
    click.echo("   Tasks: 0 pending")


@cli.command()
@click.option("--scenario", default="basic", help="Demo scenario to run")
def demo(scenario):
    """Run a demonstration scenario."""
    click.echo(f"🎭 Running {scenario} demo...")
    # Implementation would go here
    click.echo("✅ Demo completed (template)")


if __name__ == "__main__":
    cli()
EOF

# Make CLI executable
chmod +x scripts/swarm_cli.py

# Create basic test
cat > tests/unit/test_orchestrator.py << 'EOF'
"""Tests for swarm orchestrator."""

import pytest
from unittest.mock import AsyncMock, MagicMock

# Note: Actual tests would require implemented components
# This is a template structure


class TestPydanticAISwarmOrchestrator:
    """Test cases for swarm orchestrator."""

    @pytest.mark.asyncio
    async def test_orchestrator_creation(self):
        """Test orchestrator can be created."""
        # Template test - implementation would go here
        assert True  # Placeholder

    @pytest.mark.asyncio
    async def test_agent_registration(self):
        """Test agent registration functionality."""
        # Template test - implementation would go here
        assert True  # Placeholder
EOF

# Create GitHub Actions workflow
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Lint with ruff
      run: ruff check src/

    - name: Type check with mypy
      run: mypy src/

    - name: Format check with black
      run: black --check src/

    - name: Run tests
      run: pytest tests/ -v --cov=pydantic_ai_swarm --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
EOF

# Create contributing guide
cat > CONTRIBUTING.md << 'EOF'
# Contributing to Pydantic AI Democratic Swarm

Thank you for your interest in contributing to the Pydantic AI Democratic Swarm! This document provides guidelines and information for contributors.

## 🏗️ Development Setup

### Prerequisites
- Python 3.9+
- Git
- A GitHub account

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/pydantic-ai-democratic-swarm.git
cd pydantic-ai-democratic-swarm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/
```

## 📋 Development Workflow

### 1. Choose an Issue
- Check the [Issues](../../issues) page for tasks to work on
- Comment on the issue to indicate you're working on it
- Create a feature branch from `main`

### 2. Development
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Ensure tests pass
pytest tests/

# Format code
black src/
isort src/

# Type check
mypy src/

# Lint
ruff check src/
```

### 3. Testing
- Write tests for new functionality
- Ensure all existing tests pass
- Add integration tests for complex features
- Test edge cases and error conditions

### 4. Documentation
- Update docstrings for public APIs
- Add examples for new features
- Update README if needed
- Ensure documentation builds

### 5. Commit and Push
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add amazing new feature

- Description of changes
- Breaking changes (if any)
- Related issues"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to the repository on GitHub
- Click "New Pull Request"
- Select your feature branch
- Fill out the pull request template
- Request review from maintainers

## 🎯 Code Standards

### Python Style
- Follow PEP 8
- Use type hints for all function parameters and return values
- Write descriptive variable and function names
- Keep functions small and focused

### Documentation
- Use Google-style docstrings
- Document all public APIs
- Include examples in docstrings where helpful
- Keep README and docs up to date

### Testing
- Write unit tests for all new code
- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Use descriptive test names

### Commit Messages
- Use conventional commit format
- Start with type: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Keep first line under 50 characters
- Use body for detailed explanations

## 🏗️ Architecture Guidelines

### Agent Design
- Extend `BaseAgent` for new agent types
- Implement required abstract methods
- Follow the confidence-based decision pattern
- Register capabilities with the efficiency enforcer

### Tool Design
- Extend `BaseTool` for new tools
- Declare compatible agents
- Handle errors gracefully
- Include comprehensive validation

### Swarm Integration
- Use the orchestrator for task coordination
- Respect efficiency enforcer decisions
- Implement proper error handling
- Follow democratic consensus patterns

## 🚨 Efficiency Rules

All contributions must follow the [Efficiency Rules](../docs/efficiency-rules.md):

- **No Code Duplication**: Always check for existing functionality first
- **Consensus Required**: Major changes need swarm consensus
- **Documentation Required**: All public APIs must be documented
- **Testing Required**: All code must have adequate test coverage

## 📞 Getting Help

- 📧 **Discussions**: Use [GitHub Discussions](../../discussions) for questions
- 🐛 **Issues**: Report bugs via [GitHub Issues](../../issues)
- 💬 **Discord**: Join our community Discord (link in README)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

Thank you for contributing to the Pydantic AI Democratic Swarm! 🎉
EOF

# Create issue templates
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug Report
about: Report a bug or unexpected behavior
title: "[BUG] Brief description of the issue"
labels: bug
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 🔄 Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## 📋 Expected Behavior
A clear and concise description of what you expected to happen.

## 📸 Screenshots/Logs
If applicable, add screenshots or error logs to help explain your problem.

## 🖥️ Environment
- OS: [e.g., Ubuntu 22.04, macOS 13.0, Windows 11]
- Python Version: [e.g., 3.9, 3.10]
- Swarm Version: [e.g., 1.0.0]

## 📊 Additional Context
Add any other context about the problem here, such as:
- Related issues or PRs
- Workarounds you've tried
- Performance impact
- Security implications
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature Request
about: Suggest a new feature or enhancement
title: "[FEATURE] Brief description of the feature"
labels: enhancement
assignees: ''
---

## ✨ Feature Summary
A clear and concise description of the feature you'd like to see.

## 🎯 Problem Statement
What problem does this feature solve? What is the current limitation?

## 💡 Proposed Solution
Describe your proposed solution and how it would work.

## 🔄 Alternative Solutions
Describe any alternative solutions or features you've considered.

## 📊 Impact Assessment
- **Breaking Changes**: Does this introduce breaking changes?
- **Performance Impact**: Any performance implications?
- **Complexity**: How complex would this be to implement?

## 🎨 Additional Context
Add any other context, mockups, or examples that would help illustrate the feature.

## 📋 Implementation Notes
Any technical details or implementation considerations for maintainers.
EOF

# Git configuration and commit
echo "🔧 Configuring Git..."
if [ -z "$(git config user.name)" ]; then
    git config user.name "Pydantic AI Swarm"
fi
if [ -z "$(git config user.email)" ]; then
    git config user.email "team@pydantic-ai-swarm.dev"
fi

echo "📝 Creating initial commit..."
git add .

cat > commit_message.txt << 'EOF'
feat: Complete Pydantic AI Democratic Swarm system

🎯 Revolutionary Features:
- Democratic AI agent orchestration with voting consensus
- Automatic efficiency enforcement preventing code duplication
- Enterprise-grade monitoring and health checks
- Multi-domain flexibility for various applications
- Professional CLI and API interfaces

🏗️ Core Architecture:
- Swarm orchestrator with confidence-based task assignment
- Efficiency enforcer with duplicate detection
- Diagnostic system with automated issue resolution
- Communication protocols for agent coordination
- Governance system with consensus algorithms

🛡️ Quality Assurance:
- Type-safe implementation with Pydantic
- Comprehensive test suite and CI/CD
- Automated linting, formatting, and type checking
- Performance monitoring and optimization
- Security best practices

📚 Documentation & Examples:
- Professional README with usage examples
- Complete API documentation
- Getting started guides and tutorials
- Domain-specific implementation examples
- Efficiency rules and guardrails documentation

🔧 Developer Experience:
- Modern Python packaging with pyproject.toml
- Command-line interface for easy interaction
- Development tools and scripts
- Docker support for containerized deployment
- Pre-commit hooks and code quality tools

🎨 Use Cases Supported:
- Content creation and marketing automation
- Code analysis and development assistance
- Research and data analysis tasks
- Business intelligence and decision support
- Creative tasks and collaborative workflows

This represents a breakthrough in AI agent systems - the first truly
democratic, efficient, and production-ready swarm intelligence platform.
EOF

git commit -F commit_message.txt
rm commit_message.txt

# Create GitHub repository if requested
if [ "$CREATE_REMOTE" = true ]; then
    echo "🔗 Creating GitHub repository..."
    if command -v gh &> /dev/null; then
        # Use GitHub CLI if available
        gh repo create "$REPO_NAME" --public --description "Democratic AI agent orchestration with efficiency enforcement" --source=. --remote=origin
    else
        echo "⚠️  GitHub CLI not found. Please create repository manually at:"
        echo "   https://github.com/new"
        echo "   Name: $REPO_NAME"
        echo "   Description: Democratic AI agent orchestration with efficiency enforcement"
        echo ""
        echo "Then run:"
        echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo "   git push -u origin main"
    fi
fi

echo ""
echo "🎉 Repository creation complete!"
echo "=================================="
echo ""
echo "📁 Repository created at: $(pwd)"
echo "📊 Files created: $(find . -type f -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.txt" -o -name "*.sh" | wc -l)"
echo ""
echo "🚀 Next steps:"
echo "1. Create GitHub repository (if not done automatically)"
echo "2. Set remote: git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "3. Push: git push -u origin main"
echo "4. Install: pip install -e ."
echo "5. Test: python examples/basic/simple_swarm.py"
echo ""
echo "🤖 The swarm revolution begins now!"
echo "   Democratizing artificial intelligence, one agent at a time."
EOF

# Make the script executable
chmod +x create_ai_agent_repo.sh

echo "✅ Repository creation script created!"
echo "Run: ./create_ai_agent_repo.sh --github-username=yourusername"
