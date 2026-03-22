"""
Codegen Arena - Benchmark and compare AI code generation tools.

A lightweight framework for evaluating and comparing code outputs
from different AI coding assistants like Claude Code, Codex, Copilot, and more.
"""

__version__ = "0.1.0"

from .challenge import Challenge, ChallengeSet
from .evaluator import CodeEvaluator
from .arena import Arena

__all__ = ["Challenge", "ChallengeSet", "CodeEvaluator", "Arena"]
