import collections
from pathlib import Path
import time
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "10092"
EXAMPLE_ANSWER_2: Final[str] = "9021"
DAY: Final[int] = 15
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

    # answer2 = part2(sample_input=True) == EXAMPLE_ANSWER_2
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def look_ahead(
    grid: dict[tuple[int, int], str],
    start: tuple[int, int],
    direction: tuple[int, int],
    n: int,
) -> str:
    new_char_coords = (start[0] + n * direction[0], start[1] + n * direction[1])

    return grid[new_char_coords]


def update_grid(
    grid: dict[tuple[int, int], str],
    start: tuple[int, int], 
    direction: tuple[int, int], 
    items: list[str],
) -> tuple[int, int]:
    priority = {".": 0, "@": 1, "O": 2}
    sorted_items = sorted(items, key=lambda item: priority[item])
    reply: tuple[int, int] = (0, 0)
    # print(f"items to move: {items}")
    for n, char in enumerate(sorted_items):
        current = (start[0] + n * direction[0], start[1] + n * direction[1])
        # print(f"current: {current}")
        grid[current] = char
        if char == "@":
            print(f"@ goes to {current}")
            reply = current

    # print("\n")
    return reply


def update_grid_2(
    grid: dict[tuple[int, int], str],
    grid_update: list[tuple[int, int]], 
    direction: tuple[int, int],
) -> None:
    if direction == (1, 0):  # East -> max-x first
        grid_update = sorted(grid_update, key=lambda x: x[0], reverse=True)
    if direction == (-1, 0):  # West -> min-x first
        grid_update = sorted(grid_update, key=lambda x: x[0], reverse=False)
    if direction == (0, 1):  # South -> max-y first
        grid_update = sorted(grid_update, key=lambda x: x[1], reverse=True)
    if direction == (0, -1):  # North -> min-y first
        grid_update = sorted(grid_update, key=lambda x: x[1], reverse=False)
    
    print(f"{direction=}:{grid_update=}")
    for coord in grid_update:
        char = grid[coord]
        grid[coord] = "."
        grid[(coord[0] + direction[0], coord[1] + direction[1])] = char


def calculate_gps(grid: dict[tuple[int, int], str]) -> int:
    total = 0
    for (x, y), char in grid.items():
        if char != "O":
            continue

        total += (x + 100 * y)

    return total


def calculate_gps_2(grid: dict[tuple[int, int], str]) -> int:
    total = 0
    for (x, y), char in grid.items():
        if char != "[":
            continue

        total += (x + 100 * y)

    return total


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    grid_data, movements = data.split("\n\n", 1)
    movements = movements.replace("\n", "")
    grid: dict[tuple[int, int], str] = {}
    current: tuple[int, int] = (0, 0)
    for y, line in enumerate(grid_data.split("\n")):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "@":
                current = (x, y)

    direction_mapper: dict[str, tuple[int, int]] = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
    }

    # print(f"grid before: {grid}\n\n")
    for i, move in enumerate(movements, start=1):
        print(f"{move=} for {i=}")
        direction = direction_mapper[move]
        n = 1
        items: list[str] = ["@"]

        while True:
            next_char = look_ahead(grid, current, direction, n)
            if next_char == "#":
                break

            if next_char == ".":
                items.append(".")
                break
            
            items.append(next_char)
            n += 1
        
        # Update grid and next iteration
        current = update_grid(grid, current, direction, items)
    
        # print(f"grid after {i=}: \n{grid}\n\n")
    
    answer = calculate_gps(grid)
    return str(answer)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    grid_data, movements = data.split("\n\n", 1)
    movements = movements.replace("\n", "")
    grid_data = grid_data.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")

    grid: dict[tuple[int, int], str] = {}
    current: tuple[int, int] = (0, 0)
    for y, line in enumerate(grid_data.split("\n")):
        l = ""
        for x, char in enumerate(line):
            l += char
            grid[(x, y)] = char
            if char == "@":
                current = (x, y)
        print(l)

    direction_mapper: dict[str, tuple[int, int]] = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
    }

    for i, move in enumerate(movements, start=1):
        print(f"{move=} for {i=}")
        direction = direction_mapper[move]

        # Collect a list of all items that want to be moved
        grid_update: list[tuple[int, int]] = []
        to_check_queue = collections.deque([current])
        should_update = True

        while to_check_queue:
            # Grab the current location to check
            coord = to_check_queue.pop()
            grid_update.append(coord)
            current_char = grid[coord]

            # Next coordinate to inspect
            next_coord = (coord[0] + direction[0], coord[1] + direction[1])
            next_char = grid[next_coord]

            # If we hit a "#" we are doneski
            if next_char == "#":
                should_update = False
                break
            
            # If we hit a "." this path is free to move, nothing to do
            if next_char == ".":
                continue
            
            # When moving left to right we can progress normally
            if move in [">", "<"]:
                if next_char not in ["[", "]"]:
                    raise ValueError(f"weird state: {next_char=}:{direction=}")
                to_check_queue.append(next_coord)
            if move in ["^", "v"]:
                to_check_queue.append(next_coord)
                if next_char == "]":
                    # We need to add char to the left
                    neighbour_coord = (next_coord[0] - 1, next_coord[1])

                elif next_char == "[":
                    # We need to add char to the right
                    neighbour_coord = (next_coord[0] + 1, next_coord[1])
                else:
                    raise ValueError(f"weird state: {next_char=}:{direction=}")

                to_check_queue.append(neighbour_coord)
        
        if should_update:
            # Don't forget to add our robot's position
            # grid_update[current] = "@"
            print(f"updating grid with: {grid_update=}")
            update_grid_2(grid, list(set(grid_update)), direction)
            
            # Update our robot
            current = (current[0] + direction[0], current[1] + direction[1])
            print_grid(grid)

    # print_grid(grid)
    answer = calculate_gps_2(grid)
    raise ValueError(answer)
    # Your implementation goes here
    return str(answer)
 

def print_grid(grid):
    for y in range(10):
        l = ""
        for x in range(20):
            l += grid[(x, y)]
        print(l)


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
