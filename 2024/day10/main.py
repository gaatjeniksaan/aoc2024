from pathlib import Path
from typing import Final


DAY: Final[int] = 10
YEAR: Final[int] = 2024


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def looker(
        grid: dict[tuple[int, int], int],
        position: tuple[int, int],
        value: int,
    ) -> list[tuple[int, int]]:
    looksies = [
        (0, -1),  # North
        (1, 0),  # East
        (0, 1),  # South
        (-1, 0),  # West
    ]

    next_positions: list[tuple[int, int]] = []
    for looksie in looksies:
        p: tuple[int, int] = (position[0] + looksie[0], position[1] + looksie[1])
        try:
            if grid[p] == value + 1:
                next_positions.append(p)
        except KeyError:
            continue

    return next_positions


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    grid: dict[tuple[int, int], int] = {}
    starts: list[tuple[int, int]] = []
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            x_ = int(x)
            y_ = int(y)
            n = int(char)

            grid[(x_, y_)] = n

            if n == 0:
                starts.append((x_, y_))
    
    total = 0
    for zero in starts:

        value = 0
        # What positions to check
        positions = [zero]
        while value < 9:
            next_pos = []

            for pos in positions:
                next_pos.extend(looker(grid, pos, value))

            positions = next_pos
            value += 1

        total += len(set(positions))

    return total


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    grid: dict[tuple[int, int], int] = {}
    starts: list[tuple[int, int]] = []
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            x_ = int(x)
            y_ = int(y)
            n = int(char)

            grid[(x_, y_)] = n

            if n == 0:
                starts.append((x_, y_))
    
    total = 0
    for zero in starts:
        paths: list[list[tuple(int, int)]] = [
            [zero],  # Initial starting point
        ]
        value = 0

        # What positions to check
        while value < 9:
            new_paths: list[list[tuple(int, int)]] = []

            for i, path in enumerate(paths):
                last_position = path[-1]

                new_positions = looker(grid, last_position, value)

                for new_pos in new_positions:
                    new_paths.append(path + [new_pos])

            paths = new_paths
            value += 1

        total += len(paths)

    return total 


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
