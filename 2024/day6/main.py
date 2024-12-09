from collections import defaultdict
from math import dist
from pathlib import Path
from typing import Final


DAY: Final[int] = 6
YEAR: Final[int] = 2024


def main():
    solution1, distinct_positions = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2(distinct_positions)
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    # let's populate a grid (dict), (x, y) = char
    grid = defaultdict(str)
    
    # 0 == N, 1 == E, 2 == S, 3 == W, 4 == N, etc...
    direction = 0
    mapper = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
    }
    current: tuple[int, int] = (0, 0)

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "^":
                current = (x, y)
            grid[(x, y)] = char
    print(grid)
    print(current)

    # Traverse the grid:
    distinct_positions = {}
    finished = ""

    while True:
        update = mapper[direction % 4]
        next_pos = (current[0] + update[0], current[1] + update[1])
        next_char = grid[next_pos]

        if next_char == "#":
            direction += 1
            continue
        if next_char == "":
            print("finished!")
            break

        distinct_positions[current] = "V"
        print(f"{current=} -> {next_pos=} -> {next_char}")
        current = next_pos

    # Your implementation goes here
    return len(distinct_positions.keys()) + 1


def part2(distinct_positions, sample_input: bool = False) -> str:
    data = load_data(sample_input)

    # let's populate a grid (dict), (x, y) = char
    grid = defaultdict(str)
    
    # 0 == N, 1 == E, 2 == S, 3 == W, 4 == N, etc...
    direction = 0
    mapper = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
    }
    current: tuple[int, int] = (0, 0)

    # Construct all possible obstacle coordinates
    obstacle_options: list[tuple[int, int]] = [(k, v) for k, v in distinct_positions.items()]

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "^":
                current = (x, y)
            grid[(x, y)] = char
            # if char == ".":
            #     obstacle_options.append((x, y))

    n = 0
    for coord in obstacle_options:
    # for coord in [(3,6)]:
        # Run function here
        if is_endless(
            coord=coord,
            mapper=mapper,
            start_position=current,
            start_direction=direction,
            grid=grid
        ):
            n += 1

    return str(n)


def is_endless(
        coord: tuple[int, int],
        mapper,
        start_position,
        start_direction,
        grid,
    ) -> True:
    # Store every point AND direction visited.
    # If we have a match, we are in a loop.
    visited = {}
    direction = start_direction
    current = start_position

    # Update our local grid with the obstacle
    grid = dict(grid)
    grid[coord] = "#"

    while True:
        key = (current, direction % 4)
        # Have we been here before?
        if visited.get(key):
            return True

        update = mapper[direction % 4]
        next_pos = (current[0] + update[0], current[1] + update[1])
        next_char = grid.get(next_pos, "")
        visited[key] = True

        if next_char == "#":
            direction += 1
            # print(f"encountered #, changing direction to {direction}")
            continue
        if next_char == "":
            # print("encountered '': finished!")
            return False

        current = next_pos

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
