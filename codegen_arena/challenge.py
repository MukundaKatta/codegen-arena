"""
Challenge definitions for code generation benchmarks.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TestCase:
    """A single test case for validating generated code."""
    input_args: list
    expected_output: any
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "input_args": self.input_args,
            "expected_output": self.expected_output,
            "description": self.description,
        }


@dataclass
class Challenge:
    """A code generation challenge with prompt, signature, and test cases."""

    id: str
    name: str
    prompt: str
    function_name: str
    test_cases: list[TestCase]
    difficulty: str = "medium"
    category: str = "general"
    language: str = "python"
    time_limit_seconds: float = 10.0
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "name": self.name, "prompt": self.prompt,
            "function_name": self.function_name,
            "test_cases": [tc.to_dict() for tc in self.test_cases],
            "difficulty": self.difficulty, "category": self.category,
            "language": self.language,
            "time_limit_seconds": self.time_limit_seconds,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Challenge":
        """Create a Challenge from a dictionary."""
        test_cases = [TestCase(**tc) for tc in data.get("test_cases", [])]
        return cls(
            id=data["id"], name=data["name"], prompt=data["prompt"],
            function_name=data["function_name"], test_cases=test_cases,
            difficulty=data.get("difficulty", "medium"),
            category=data.get("category", "general"),
            language=data.get("language", "python"),
            time_limit_seconds=data.get("time_limit_seconds", 10.0),
            tags=data.get("tags", []),
        )


class ChallengeSet:
    """A collection of code generation challenges."""

    def __init__(self, name: str = "default"):
        self.name = name
        self.challenges: list[Challenge] = []

    def add(self, challenge: Challenge) -> None:
        self.challenges.append(challenge)

    def load_from_json(self, path: str) -> None:
        with open(path) as f:
            data = json.load(f)
        for item in data.get("challenges", []):
            self.challenges.append(Challenge.from_dict(item))

    def save_to_json(self, path: str) -> None:
        data = {"name": self.name, "challenges": [c.to_dict() for c in self.challenges]}
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def filter_by_difficulty(self, difficulty: str) -> list[Challenge]:
        return [c for c in self.challenges if c.difficulty == difficulty]

    def filter_by_category(self, category: str) -> list[Challenge]:
        return [c for c in self.challenges if c.category == category]

    def __len__(self) -> int:
        return len(self.challenges)

    def __iter__(self):
        return iter(self.challenges)
