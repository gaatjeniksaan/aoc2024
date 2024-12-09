import functools
import operator
from pathlib import Path
from typing import Final


DAY: Final[int] = 2
YEAR: Final[int] = 2024


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    total = 0
    data = load_data(sample_input).split("\n")

    for line in data:
        items = [int(c) for c in line.split("x")]
        items = sorted(items)
        total += 3 * items[0] * items[1]
        total += 2 * items[0] * items[2]
        total += 2 * items[1] * items[2]

    return total


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    
    total = 0
    data = load_data(sample_input).split("\n")

    for line in data:
        items = [int(c) for c in line.split("x")]
        items = sorted(items)
        total += 2 * items[0] + 2 * items[1]
        total += functools.reduce(operator.mul, items, 1)

    return total 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
