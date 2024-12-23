import collections
from functools import cache
from pathlib import Path
import time
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "6"
EXAMPLE_ANSWER_2: Final[str] = "16"  # Provide this yourself
DAY: Final[int] = 19
YEAR: Final[int] = 2024


def main():
    answer1 = part1(sample_input=True)
    assert answer1 == EXAMPLE_ANSWER_1, f"calculated answer '{answer1}' != expected answer '{EXAMPLE_ANSWER_1}'"
    start_time = time.time()
    solution1 = part1()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part1: {solution1}")
    print(f"Execution time for part1: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    answer2 = part2(sample_input=True)
    assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n\n")

    options = data[0].split(", ")
    towels = data[1].split("\n")

    possible = 0
    s = "aaa"
    s.lstrip()

    for towel in towels:
        queue = collections.deque()
        queue.append(towel)
        while queue:
            subtowel = queue.pop()
            if subtowel == "":
                possible += 1
                break
            for option in options:
                if not subtowel.startswith(option):
                    continue
                new_sub_towel = subtowel[len(option):]
                queue.append(new_sub_towel)

    return str(possible)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n\n")

    options = data[0].split(", ")
    towels = data[1].split("\n")

    possible = 0

    @cache
    def has_match(towel) -> int:
        # We have subdivided enough now, end of recursion
        if towel == "":
            return 1
        print(towel)
        
        # Collect potential matches - just like part1
        matches = []
        for option in options:
            if not towel.startswith(option):
                continue
            matches.append(towel[len(option):])
        
        return sum(has_match(t) for t in matches)

    for towel in towels:
        possible += has_match(towel)

    return str(possible)
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
