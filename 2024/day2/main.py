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


def part1(sample_input: bool = False) -> int:
    data = load_data(sample_input)

    safes: int = 0
    lines = data.split("\n")
    numbers = [[int(x) for x in line.split()] for line in lines]

    for number in numbers:
        diffs = [j-i for i, j in zip(number[:-1], number[1:])]
        
        safes += safe(diffs)
    return safes


def safe(diffs: list[int]) -> bool:
    ascending = all(1 <= d <= 3 for d in diffs)
    descending = all(-1 >= d >= -3 for d in diffs)

    return any([ascending, descending])


def part2(sample_input: bool = False) -> int:
    data = load_data(sample_input)
    
    safes: int = 0
    lines = data.split("\n")
    numbers = [[int(x) for x in line.split()] for line in lines]

    for number in numbers:
        options: list[list[int]] = [number[0:i] + number[i+1:] for i in range(len(number))]
        # Also check for the OG list
        options.append(number)
        
        diffs: list[list[int]] = []
        for option in options:
            diffs.append([j-i for i, j in zip(option[:-1], option[1:])])
        
        if any(safe(diff) for diff in diffs):
            safes += 1
    return safes
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
