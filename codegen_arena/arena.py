"""
Arena module - the main competition runner.

Runs code generation challenges across multiple models,
collects results, and produces comparison reports.
"""

import json
import time
from dataclasses import dataclass, field

from .challenge import Challenge, ChallengeSet
from .evaluator import CodeEvaluator, EvaluationResult


@dataclass
class ModelScore:
    """Aggregated score for one model across all challenges."""
    model_name: str
    challenges_attempted: int
    challenges_passed: int
    total_tests_passed: int
    total_tests: int
    overall_pass_rate: float
    avg_code_length: float
    avg_execution_time_ms: float
    score: float

    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "challenges_attempted": self.challenges_attempted,
            "challenges_passed": self.challenges_passed,
            "total_tests_passed": self.total_tests_passed,
            "total_tests": self.total_tests,
            "overall_pass_rate": round(self.overall_pass_rate, 4),
            "avg_code_length": round(self.avg_code_length, 1),
            "avg_execution_time_ms": round(self.avg_execution_time_ms, 2),
            "score": round(self.score, 2),
        }


class Arena:
    """The main competition arena for comparing AI code generators."""

    def __init__(self, timeout: float = 10.0):
        self.evaluator = CodeEvaluator(timeout=timeout)
        self.challenge_set = ChallengeSet()
        self.results: dict[str, list[EvaluationResult]] = {}

    def add_challenge(self, challenge: Challenge) -> None:
        self.challenge_set.add(challenge)

    def load_challenges(self, path: str) -> None:
        self.challenge_set.load_from_json(path)

    def get_challenge(self, challenge_id: str) -> Challenge:
        for c in self.challenge_set:
            if c.id == challenge_id:
                return c
        raise ValueError(f"Challenge '{challenge_id}' not found")

    def submit(self, model_name: str, challenge_id: str, code: str) -> EvaluationResult:
        """Submit a code solution for evaluation."""
        challenge = self.get_challenge(challenge_id)
        result = self.evaluator.evaluate(challenge, code, model_name)
        if model_name not in self.results:
            self.results[model_name] = []
        self.results[model_name].append(result)
        return result

    def get_model_score(self, model_name: str) -> ModelScore:
        """Calculate the aggregate score for a model."""
        if model_name not in self.results:
            raise ValueError(f"No results for model '{model_name}'")
        results = self.results[model_name]
        total_passed = sum(r.tests_passed for r in results)
        total_tests = sum(r.tests_total for r in results)
        challenges_passed = sum(1 for r in results if r.is_correct)
        avg_length = sum(r.code_length for r in results) / len(results)
        avg_time = sum(r.avg_execution_time_ms for r in results) / len(results)
        pass_rate = total_passed / total_tests if total_tests > 0 else 0
        # Composite: correctness (70%) + brevity (15%) + speed (15%)
        score = (pass_rate * 70) + (max(0, (1 - avg_length / 2000)) * 15) + (max(0, (1 - avg_time / 100)) * 15)
        return ModelScore(
            model_name=model_name, challenges_attempted=len(results),
            challenges_passed=challenges_passed,
            total_tests_passed=total_passed, total_tests=total_tests,
            overall_pass_rate=pass_rate, avg_code_length=avg_length,
            avg_execution_time_ms=avg_time, score=score)

    def leaderboard(self) -> list[ModelScore]:
        """Generate a leaderboard sorted by score."""
        scores = [self.get_model_score(name) for name in self.results]
        scores.sort(key=lambda s: s.score, reverse=True)
        return scores

    def leaderboard_table(self) -> str:
        """Generate a formatted leaderboard table."""
        scores = self.leaderboard()
        lines = [
            "Codegen Arena Leaderboard",
            "=" * 70,
            f"{'Rank':<6}{'Model':<20}{'Score':<10}{'Pass Rate':<12}{'Challenges':<12}{'Avg Time':<10}",
            "-" * 70,
        ]
        for i, s in enumerate(scores, 1):
            lines.append(
                f"{i:<6}{s.model_name:<20}{s.score:<10.1f}"
                f"{s.overall_pass_rate * 100:<12.1f}"
                f"{s.challenges_passed}/{s.challenges_attempted:<11}"
                f"{s.avg_execution_time_ms:<10.2f}")
        return "\n".join(lines)

    def leaderboard_markdown(self) -> str:
        """Generate a Markdown leaderboard table."""
        scores = self.leaderboard()
        lines = [
            "# Codegen Arena Leaderboard", "",
            "| Rank | Model | Score | Pass Rate | Challenges | Avg Time (ms) |",
            "|------|-------|-------|-----------|------------|---------------|",
        ]
        for i, s in enumerate(scores, 1):
            lines.append(
                f"| {i} | {s.model_name} | {s.score:.1f} "
                f"| {s.overall_pass_rate * 100:.1f}% "
                f"| {s.challenges_passed}/{s.challenges_attempted} "
                f"| {s.avg_execution_time_ms:.2f} |")
        return "\n".join(lines)

    def export_results(self, path: str) -> None:
        """Export all results to a JSON file."""
        data = {
            "leaderboard": [s.to_dict() for s in self.leaderboard()],
            "details": {m: [r.to_dict() for r in rs] for m, rs in self.results.items()},
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
