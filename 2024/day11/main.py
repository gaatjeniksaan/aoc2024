from functools import cache
from pathlib import Path
from typing import Counter, Final
import time  # Import the time module


DAY: Final[int] = 11
YEAR: Final[int] = 2024


def main():
    start_time = time.time()
    solution1 = part1()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part1: {solution1}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


@cache
def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]  # The stone "becomes" 1

    stringed = str(stone)
    length = len(stringed)
    if length % 2 == 0:
        half = length // 2
        l = stringed[:half].lstrip("0")
        r = stringed[half:].lstrip("0")

        # If we have all 0's we will be left with an empty string
        l = int(l) if l else 0
        r = int(r) if r else 0

        return [l, r]
    
    return [stone * 2024]


def process(stones: list[int], n: int) -> int:
    counter = Counter(stones)
    
    for _ in range(n):
        sub_counter = Counter()

        for number, count in counter.items():
            new_numbers = blink(number)
            for nn in new_numbers:
                sub_counter[nn] += count

        counter = sub_counter
    
    return counter.total()


def part1(sample_input: bool = True) -> str:
    data = load_data(sample_input)

    stones = data.split(" ")
    stones = [int(stone) for stone in stones]
    # print(f"starting with: {stones}")

    return process(stones, 25)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    stones = data.split(" ")
    stones = [int(stone) for stone in stones]
    
    return process(stones, 75)
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
