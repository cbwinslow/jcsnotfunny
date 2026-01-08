"""Compatibility shim to expose the reference practical_toolset implementation for tests.

This module intentionally re-exports the implementation from `scripts/toolsets/practical_toolset.py`
so tests that add `scripts/` to `sys.path` will import this implementation rather than the top-level
`toolsets` package used for production code.
"""
from .practical_toolset import *  # noqa: F401,F403

# Provide basic compatibility exceptions for tests (kept intentionally small)
class ToolError(Exception):
    pass

class ToolConfigError(ToolError):
    pass

class ValidationError(ToolError):
    pass

class FatalError(ToolError):
    pass

__all__ = [
    name for name in dir() if not name.startswith("_")
]
