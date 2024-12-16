from pathlib import Path
from shutil import move
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

    answer2 = part2(sample_input=True) == EXAMPLE_ANSWER_2
    assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
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
    start: tuple[int, int], 
    direction: tuple[int, int], 
    items: list[str],
) -> tuple[int, int]:
    priority = {".": 0, "@": 1}
    if direction == (1, 0):
        # We are moving right
        priority["["] = 3
        
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


def calculate_gps(grid: dict[tuple[int, int], str]) -> int:
    total = 0
    for (x, y), char in grid.items():
        if char != "O":
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
        current = update_grid_2(grid, current, direction, items)
    
        # print(f"grid after {i=}: \n{grid}\n\n")
    
    answer = calculate_gps(grid)
    
    # Your implementation goes here
    answer = "geenidee"
    return answer
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
