"""
Code evaluation engine for the arena.

Safely executes generated code, runs test cases, and scores
the output for correctness, performance, and code quality.
"""

import time
import traceback
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TestResult:
    """Result of running a single test case."""
    passed: bool
    input_args: list
    expected: any
    actual: any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


@dataclass
class EvaluationResult:
    """Complete evaluation result for one submission."""
    challenge_id: str
    model_name: str
    code: str
    tests_passed: int
    tests_total: int
    pass_rate: float
    avg_execution_time_ms: float
    total_time_ms: float
    test_results: list[TestResult] = field(default_factory=list)
    compile_error: Optional[str] = None
    code_length: int = 0

    def to_dict(self) -> dict:
        return {
            "challenge_id": self.challenge_id,
            "model_name": self.model_name,
            "code_length": self.code_length,
            "tests_passed": self.tests_passed,
            "tests_total": self.tests_total,
            "pass_rate": round(self.pass_rate, 4),
            "avg_execution_time_ms": round(self.avg_execution_time_ms, 2),
            "total_time_ms": round(self.total_time_ms, 2),
            "compile_error": self.compile_error,
        }

    @property
    def is_correct(self) -> bool:
        return self.tests_passed == self.tests_total and self.tests_total > 0


class CodeEvaluator:
    """Evaluates generated code against challenge test cases."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def evaluate(self, challenge, code: str, model_name: str = "unknown") -> EvaluationResult:
        """Evaluate generated code against a challenge's test cases."""
        namespace = {}
        try:
            exec(code, namespace)
        except Exception as e:
            return EvaluationResult(
                challenge_id=challenge.id, model_name=model_name, code=code,
                tests_passed=0, tests_total=len(challenge.test_cases),
                pass_rate=0.0, avg_execution_time_ms=0.0, total_time_ms=0.0,
                compile_error=f"{type(e).__name__}: {e}", code_length=len(code))

        func = namespace.get(challenge.function_name)
        if func is None:
            return EvaluationResult(
                challenge_id=challenge.id, model_name=model_name, code=code,
                tests_passed=0, tests_total=len(challenge.test_cases),
                pass_rate=0.0, avg_execution_time_ms=0.0, total_time_ms=0.0,
                compile_error=f"Function '{challenge.function_name}' not found",
                code_length=len(code))

        test_results = []
        total_time = 0.0
        for tc in challenge.test_cases:
            start = time.perf_counter()
            try:
                actual = func(*tc.input_args)
                elapsed_ms = (time.perf_counter() - start) * 1000
                passed = actual == tc.expected_output
                test_results.append(TestResult(
                    passed=passed, input_args=tc.input_args,
                    expected=tc.expected_output, actual=actual,
                    execution_time_ms=elapsed_ms))
            except Exception as e:
                elapsed_ms = (time.perf_counter() - start) * 1000
                test_results.append(TestResult(
                    passed=False, input_args=tc.input_args,
                    expected=tc.expected_output,
                    error=f"{type(e).__name__}: {e}",
                    execution_time_ms=elapsed_ms))
            total_time += elapsed_ms

        passed = sum(1 for tr in test_results if tr.passed)
        total = len(test_results)
        avg_time = total_time / total if total > 0 else 0.0

        return EvaluationResult(
            challenge_id=challenge.id, model_name=model_name, code=code,
            tests_passed=passed, tests_total=total,
            pass_rate=passed / total if total > 0 else 0.0,
            avg_execution_time_ms=avg_time, total_time_ms=total_time,
            test_results=test_results, code_length=len(code))
