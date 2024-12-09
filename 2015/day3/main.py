from collections import defaultdict
from pathlib import Path
from typing import Final


DAY: Final[int] = 3
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

    loc = (0, 0)
    locations = defaultdict(int)
    locations[loc] += 1

    mapper = {
        "v": (0, -1),
        "^": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
    }

    for char in data:
        delta = mapper[char]
        loc = (loc[0] + delta[0], loc[1] + delta[1])
        locations[loc] += 1

    return len([x for x in locations.values() if x > 1])


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
