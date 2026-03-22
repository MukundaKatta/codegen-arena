"""
Example: Run a codegen arena competition.

This demo shows how to create challenges, submit code from
different "models", and generate a leaderboard.
"""

from codegen_arena import Arena, Challenge
from codegen_arena.challenge import TestCase


def main():
    # Create the arena
    arena = Arena(timeout=5.0)

    # Define a challenge
    two_sum = Challenge(
        id="two-sum",
        name="Two Sum",
        prompt="Write a function that finds two numbers adding to target",
        function_name="two_sum",
        difficulty="easy",
        category="arrays",
        test_cases=[
            TestCase([2, 7, 11, 15], 9, [0, 1], "Basic case"),
            TestCase([3, 2, 4], 6, [1, 2], "Middle elements"),
            TestCase([3, 3], 6, [0, 1], "Duplicates"),
        ],
    )
    arena.add_challenge(two_sum)

    palindrome = Challenge(
        id="palindrome",
        name="Palindrome Check",
        prompt="Check if a string is a palindrome",
        function_name="is_palindrome",
        difficulty="easy",
        category="strings",
        test_cases=[
            TestCase(["racecar"], True, "Simple palindrome"),
            TestCase(["hello"], False, "Not a palindrome"),
            TestCase([""], True, "Empty string"),
        ],
    )
    arena.add_challenge(palindrome)

    # Simulate submissions from different "models"
    # Model A: Claude-style solution (clean, well-structured)
    claude_two_sum = '''
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
'''

    claude_palindrome = '''
def is_palindrome(s):
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
'''

    # Model B: Codex-style solution (more verbose)
    codex_two_sum = '''
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
'''

    codex_palindrome = '''
def is_palindrome(s):
    filtered = ""
    for char in s:
        if char.isalpha() or char.isdigit():
            filtered += char.lower()
    left = 0
    right = len(filtered) - 1
    while left < right:
        if filtered[left] != filtered[right]:
            return False
        left += 1
        right -= 1
    return True
'''

    # Submit solutions
    print("Submitting solutions...\n")

    r1 = arena.submit("claude-code", "two-sum", claude_two_sum)
    print(f"Claude - Two Sum: {r1.tests_passed}/{r1.tests_total} passed")

    r2 = arena.submit("claude-code", "palindrome", claude_palindrome)
    print(f"Claude - Palindrome: {r2.tests_passed}/{r2.tests_total} passed")

    r3 = arena.submit("codex", "two-sum", codex_two_sum)
    print(f"Codex - Two Sum: {r3.tests_passed}/{r3.tests_total} passed")

    r4 = arena.submit("codex", "palindrome", codex_palindrome)
    print(f"Codex - Palindrome: {r4.tests_passed}/{r4.tests_total} passed")

    # Print leaderboard
    print("\n")
    print(arena.leaderboard_table())

    # Print markdown version
    print("\n")
    print(arena.leaderboard_markdown())


if __name__ == "__main__":
    main()
