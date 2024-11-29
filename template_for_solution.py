from pathlib import Path
from typing import Final


DAY: Final[int] = 1  # This will be regex/replaced
YEAR: Final[int] = 2024


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    # Your implementation goes here
    answer = "geenidee"
    return answer


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    
    # Your implementation goes here
    answer = "geenidee"
    return answer
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
