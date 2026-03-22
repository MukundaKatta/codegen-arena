# codegen-arena

A lightweight Python framework to benchmark and compare AI code generation tools side by side. Pit Claude Code against Codex, Copilot, and more on real coding challenges.

## Why codegen-arena?

The AI coding tool landscape is evolving fast. New models ship weekly, each claiming to be the best at writing code. But how do you actually compare them? codegen-arena gives you a structured, reproducible way to evaluate code generation quality across multiple dimensions:

- **Correctness** - Does the generated code pass test cases?
- **Speed** - How fast does the code execute?
- **Brevity** - How concise is the solution?

## Features

- Define coding challenges with test cases (or load from JSON)
- Submit solutions from any number of "models" or sources
- Automatic code evaluation with sandboxed execution
- Composite scoring: 70% correctness, 15% brevity, 15% speed
- Leaderboard generation in plain text and Markdown
- Export results to JSON for further analysis
- Built-in starter pack with 5 classic challenges
- Zero external dependencies - pure Python standard library

## Quick Start

```bash
# Clone the repo
git clone https://github.com/MukundaKatta/codegen-arena.git
cd codegen-arena

# Run the example
python examples/run_arena.py
```

## Usage

```python
from codegen_arena import Arena, Challenge
from codegen_arena.challenge import TestCase

# Create an arena
arena = Arena(timeout=5.0)

# Define a challenge
challenge = Challenge(
    id="two-sum",
    name="Two Sum",
    prompt="Find two numbers that add to target",
    function_name="two_sum",
    difficulty="easy",
    category="arrays",
    test_cases=[
        TestCase([2, 7, 11, 15], 9, [0, 1], "Basic case"),
        TestCase([3, 2, 4], 6, [1, 2], "Middle elements"),
    ],
)
arena.add_challenge(challenge)

# Submit a solution
result = arena.submit("my-model", "two-sum", """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []
""")

print(f"Passed: {result.tests_passed}/{result.tests_total}")
print(arena.leaderboard_table())
```

## Loading Challenges from JSON

```python
from codegen_arena.challenge import ChallengeSet

challenges = ChallengeSet.from_json("challenges/starter_pack.json")
for challenge in challenges.filter_by_difficulty("easy"):
    print(f"  {challenge.name} ({challenge.category})")
```

## Starter Challenges

The included `starter_pack.json` contains 5 challenges across difficulty levels:

| Challenge | Difficulty | Category |
|-----------|-----------|----------|
| Two Sum | Easy | Arrays |
| Palindrome Check | Easy | Strings |
| Flatten Nested List | Medium | Recursion |
| Group Anagrams | Medium | Strings |
| LRU Cache | Hard | Data Structures |

## Scoring

Each submission gets a composite score (0-100) based on:

- **Correctness (70%)** - Percentage of test cases passed
- **Brevity (15%)** - Shorter solutions score higher (measured in characters)
- **Speed (15%)** - Faster execution scores higher

## Project Structure

```
codegen-arena/
  codegen_arena/
    __init__.py          # Package exports
    challenge.py         # Challenge and TestCase definitions
    evaluator.py         # Code execution and evaluation engine
    arena.py             # Main arena with scoring and leaderboards
  challenges/
    starter_pack.json    # 5 built-in coding challenges
  examples/
    run_arena.py         # Demo: Claude vs Codex showdown
  setup.py
  requirements.txt
  LICENSE
```

## Requirements

- Python 3.10+
- No external dependencies

## License

MIT License - see [LICENSE](LICENSE) for details.
