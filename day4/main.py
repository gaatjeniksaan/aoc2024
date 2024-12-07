from pathlib import Path
from typing import Final


DAY: Final[int] = 4
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

    lines = data.split("\n")
    print(lines)

    xmas = 0
    coords = {}

    max_i = 0
    max_j = 0
    for i, line in enumerate(lines):
        if i > max_i:
            max_i = i
        for j, char in enumerate(line):
            if j > max_j:
                max_j = j
            coords[(i, j)] = char
        if i >= 3:
            # We can do lookback for verticals and diagonals
            pass
        
        xmas += line.count("XMAS")
        xmas += line.count("SAMX")

    # i == row!
    # j == column!
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            vertical = (
                coords.get((i, j), "") + 
                coords.get((i+1, j), "") +
                coords.get((i+2, j), "") +
                coords.get((i+3,j), "")
            )

            diagonal_right = (
                coords.get((i, j), "") + 
                coords.get((i+1, j+1), "") +
                coords.get((i+2, j+2), "") +
                coords.get((i+3,j+3), "")
            )

            diagonal_left = (
                coords.get((i, j), "") + 
                coords.get((i+1, j-1), "") +
                coords.get((i+2, j-2), "") +
                coords.get((i+3,j-3), "")

            )
            # print(f"{diagonal_right=}")
            # print(f"{diagonal_left=}")
            print(f"{vertical=}, {i, j}")

            if vertical == "XMAS" or vertical == "SAMX":
                print(f"found vertical {vertical} for {(i, j)}")
                xmas += 1
            if diagonal_left == "XMAS" or diagonal_left == "SAMX":
                xmas += 1
            if diagonal_right == "XMAS" or diagonal_right == "SAMX":
                xmas += 1


    # Your implementation goes here
    return xmas


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    lines = data.split("\n")
    print(lines)

    xmas = 0
    coords = {}

    max_i = 0
    max_j = 0
    for i, line in enumerate(lines):
        if i > max_i:
            max_i = i
        for j, char in enumerate(line):
            if j > max_j:
                max_j = j
            coords[(i, j)] = char
    
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            right = (
                coords.get((i, j), "") + 
                coords.get((i+1, j+1), "") +
                coords.get((i+2, j+2), "")
            )

            left = (
                coords.get((i, j + 2), "") + 
                coords.get((i + 1, j + 1), "") + 
                coords.get((i + 2, j), "")
            )

            if left in ("MAS", "SAM") and right in ("MAS", "SAM"):
                xmas += 1

    return xmas
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
