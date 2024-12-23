import heapq
from pathlib import Path
import time
from typing import Final

from dataclasses import dataclass

import aocd


EXAMPLE_ANSWER_1: Final[str] = "NO EXAMPLE ANSWER PROVIDED"
EXAMPLE_ANSWER_2: Final[str] = "285"  # Provide this yourself
DAY: Final[int] = 20
YEAR: Final[int] = 2024
MIN_X: Final[int] = 0
MIN_Y: Final[int] = 0


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

    answer2 = part2(sample_input=True)
    assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def look_around(
    grid: dict[tuple[int, int], str],
    coord: tuple[int, int],
) -> list[tuple[int, int]]:
    
    new_positions: list[tuple[int, int]] = []
    
    for change in [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]:
        new_coord = (coord[0] + change[0], coord[1] + change[1])
        if grid[new_coord] == "#":
            continue
        new_positions.append(new_coord)

    return new_positions


def solve_grid(
    grid: dict[tuple[int, int], str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[tuple[int, int]]:
    """solve_grid solves the grid normally and return the minimum number of steps.
    
    This can be used as a reference point for determining how many picoseconds
    have been saved.
    """
    queue: list[tuple[int, tuple[int, int]]] = []
    heapq.heappush(queue, (0, start))
    visited: list[tuple[int, int]] = []

    while queue:
        steps, coord = heapq.heappop(queue)
        if coord in visited:
            continue
        visited.append(coord)

        if coord == end:
            print("found shortest normal path")
            return visited

        new_coords = look_around(grid, coord)
        for new_coord in new_coords:
            if new_coord in visited:
                continue
            heapq.heappush(queue, (steps + 1, new_coord))


def cheat(
    grid: dict[tuple[int, int], str],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for change in [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]:
        first_new_coord = (position[0] + change[0], position[1] + change[1])
        if grid[first_new_coord] != "#":
            # Nothing to cheat
            continue
        
        second_new_coord = (position[0] + 2*change[0], position[1] + 2*change[1])
        if grid.get(second_new_coord, "") != ".":
            # Another wall or out of grid
            continue

        result.append(second_new_coord)

    return result


def generate_coordinates(coord: tuple[int, int], max_x: int, max_y: int) -> list[tuple[int, int]]:
    min_distance = 2
    max_distance = 20
    min_x = 0
    min_y = 0

    coordinates: list[tuple[int, int]] = []
    for distance in range(min_distance, max_distance + 1):
        for dx in range(-distance, distance + 1):
            dy = distance - abs(dx)
            for dy_offset in [-dy, dy]:
                new_x = coord[0] + dx
                new_y = coord[1] + dy_offset
                # Check if the new coordinate is within bounds
                if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
                    coordinates.append((new_x, new_y))
    # Sort so we check furthers coordinates first
    # Higher change for a hit (I think...).
    return sorted(coordinates, key=lambda x: x[0] + x[1], reverse=True)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    grid = {}
    start: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (0, 0)
    end: tuple[int, int]
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "S":
                start = (x, y)
            if char == "E":
                end = (x, y)
                grid[(x, y)] = "."
    
    print(grid)
    print(f"{start=}:{end=}")

    normal_path = solve_grid(grid, start, end)
    max_steps = len(normal_path)
    threshold = 100
    n_cheats = 0

    for i, position in enumerate(normal_path):
        # Check can we cheat?
        cheat_coords = cheat(grid, position)
        for cheat_coord in cheat_coords:
            index = normal_path.index(cheat_coord)
            saved_steps = (index - i - 2)
            if saved_steps >= threshold:
                print(f"{saved_steps=}:{cheat_coord=}")
                n_cheats += 1

    # Your implementation goes here
    return n_cheats


# def part2(sample_input: bool = False) -> str:
#     data = load_data(sample_input)
#     grid = {}
#     start: tuple[int, int] = (0, 0)
#     end: tuple[int, int] = (0, 0)
#     for y, line in enumerate(data.split("\n")):
#         # max_y = max(max_y, y)
#         for x, char in enumerate(line):
#             # max_x = max(max_x, x)

#             grid[(x, y)] = char
#             if char == "S":
#                 start = (x, y)
#             if char == "E":
#                 end = (x, y)
#                 grid[(x, y)] = "."
    
#     normal_path = solve_grid(grid, start, end)
#     full_steps = len(normal_path)
#     n_cheats = 20
#     total_cheats = 0
#     threshold = 50
#     for start in normal_path:
#         print(f"{start=}")
#         for end in normal_path[::-1]:
#             distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
#             if distance > n_cheats:
#                 # Not cheatable
#                 continue
#             si = normal_path.index(start)
#             ei = normal_path.index(end)
#             if si >= ei:
#                 break

#             total_steps_cheat = len(normal_path[:si]) + len(normal_path[ei:]) + distance - 1
#             if (full_steps - total_steps_cheat) >= threshold:
#                 total_cheats += 1

#     return str(total_cheats)


# def part2(sample_input: bool = True) -> str:
#     data = load_data(sample_input)
#     grid = {}
#     start: tuple[int, int] = (0, 0)
#     end: tuple[int, int] = (0, 0)
#     end: tuple[int, int]
#     max_x = 0
#     max_y = 0
#     for y, line in enumerate(data.split("\n")):
#         max_y = max(max_y, y)
#         for x, char in enumerate(line):
#             max_x = max(max_x, x)

#             grid[(x, y)] = char
#             if char == "S":
#                 start = (x, y)
#             if char == "E":
#                 end = (x, y)
#                 grid[(x, y)] = "."
    
#     normal_path = solve_grid(grid, start, end)
#     max_steps = len(normal_path)
#     threshold = 70
#     valid_cheats: set[tuple[int, int]] = set()

#     for i, position in enumerate(normal_path):
#         # Check can we cheat?
#         cheat_coords = generate_coordinates(position, max_x, max_y)
        
#         running = True
#         for cheat_coord in cheat_coords:
            
#             try:
#                 index = normal_path.index(cheat_coord)
#             except ValueError:
#                 continue
            
#             steps = abs(position[0] - cheat_coord[0]) + abs(position[1] - cheat_coord[1])
#             saved_steps = (index - i - steps)
#             if saved_steps >= threshold:
#                 print(f"{saved_steps=}:{position=}:{cheat_coord=}")
#                 valid_cheats.add(position)
#                 break
#     raise ValueError(f"{len(valid_cheats)=}")

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
