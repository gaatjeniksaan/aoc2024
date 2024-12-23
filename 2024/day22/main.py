from collections import Counter
from functools import cache
from pathlib import Path
import time
from typing import Final
import sys

import aocd


EXAMPLE_ANSWER_1: Final[str] = "37327623"
EXAMPLE_ANSWER_2: Final[str] = "23"  # Provide this yourself
DAY: Final[int] = 22
YEAR: Final[int] = 2024


def main():
    # answer1 = part1(sample_input=True)
    # assert answer1 == EXAMPLE_ANSWER_1, f"calculated answer '{answer1}' != expected answer '{EXAMPLE_ANSWER_1}'"
    # start_time = time.time()
    # solution1 = part1()
    # end_time = time.time()

    # elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    # print(f"solution for part1: {solution1}")
    # print(f"Execution time for part1: {elapsed_time_ms:.2f} ms")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    # answer2 = part2(sample_input=True)
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


@cache
def mix(secret_number: int, n: int) -> int:
    return secret_number ^ n


@cache
def prune(secret_number: int) -> int:
    return secret_number % 16777216 


@cache
def iterate(n: int) -> int:
    # Step 1
    n ^= n * 64
    n %= 16777216

    # Step 2
    n ^= n // 32
    n %= 16777216

    # Step 3
    n ^= n * 2048
    n %= 16777216
    return n


def part1(sample_input: bool = False) -> str:
    data = [int(x) for x in load_data(sample_input).split()]
    total = 0
    for number in data:
        result = number
        for _ in range(2000):
            result = iterate(result)
        total += result        

    return str(total)


def part2(sample_input: bool = False) -> str:
    data = [int(x) for x in load_data(sample_input).split()]
    c = Counter()

    for number in data:
        result = number
        previous_bananas: int | None = None
        deltas: list[int] = []
        seen: dict[tuple[int, ...], int] = {}
        delta: int

        for _ in range(2000):
            bananas = result % 10

            if previous_bananas is not None:
                delta = bananas - previous_bananas
                deltas.append(delta)
            # print(f"{bananas=}:{previous_bananas=}:{delta=}")
            previous_bananas = bananas

            last_four = tuple(deltas[-4::])
            result = iterate(result)

            if len(last_four) < 4:
                continue
            if last_four not in seen:
                seen[last_four] = bananas

        c.update(seen)
    answer = str(c.most_common(10)[0][1])
    raise ValueError(answer)
    return 
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
