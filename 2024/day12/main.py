from collections import defaultdict
from itertools import count
from re import sub
import time
from pathlib import Path
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "140"
EXAMPLE_ANSWER_2: Final[str] = "1206"  # Provide this yourself
DAY: Final[int] = 12  # This will be regex/replaced
YEAR: Final[int] = 2024


def main():
    answer1 = part1(sample_input=True)
    # assert answer1 == EXAMPLE_ANSWER_1, f"calculated answer '{answer1}' != expected answer '{EXAMPLE_ANSWER_1}'"
    start_time = time.time()
    solution1 = part1()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part1: {solution1}")
    print(f"Execution time for part1: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    answer2 = part2(sample_input=True)
    assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def cleanse_grid(grid: dict[tuple[int, int], str], coords: list[tuple[int, int]]):
    for coord in coords:
        grid[coord] = "."


def get_neighbours(grid: dict[tuple[int, int], str], coord: tuple[int, int], value: str) -> list[tuple[int, int]]:
    looksies = [
        (0, -1),  # N
        (1, 0),   # E
        (0, 1),   # S
        (-1, 0),  # W
    ]

    neighbours: list[tuple[int, int]] = []
    for look in looksies:
        neighbour_coord = (coord[0] + look[0], coord[1] + look[1])
        neighbour_value = grid.get(neighbour_coord)
        if neighbour_value == value:
            neighbours.append(neighbour_coord)
    
    return neighbours


def calculate_price_part1(coords: list[tuple[int, int]]) -> int:
    looksies = [
        (0, -1),  # N
        (1, 0),   # E
        (0, 1),   # S
        (-1, 0),  # W
    ]
    edges = 0
    n = len(coords)

    for coord in coords:
        for look in looksies:
            new_coord = (coord[0] + look[0], coord[1] + look[1])
            if not new_coord in coords:
                edges += 1
    
    return n * edges


def check_conditions_bitwise(items: list[bool]) -> bool:
    state = (items[0] << 2) | (items[1] << 1) | items[2]
    result_map = {
        0b000: True,
        0b101: True,
        0b100: False,
        0b001: False,
        0b010: True,
        0b111: False,
    }
    return result_map.get(state, False)


def count_corners(grid: list[tuple[int, int]], coord: tuple[int, int]) -> list[tuple[int, int]]:
    corners = 0
    
    # Diagnonal always goes in the middle
    ne = [(-1, 0), (-1, -1), (0, -1)]
    nw = [(0, -1), (1, -1), (1, 0)]
    se = [(1,0), (1, 1), (0, 1)]
    sw = [(0, 1), (-1, 1), (-1, 0)]

    corner_checks = [ne, nw, se, sw]
    
    for corner_check in corner_checks:
        result = []
        for adjust in corner_check:
            coord_to_check = (coord[0] + adjust[0], coord[1] + adjust[1])
            result.append(coord_to_check in grid)
        if check_conditions_bitwise(result):
            corners += 1
    
    return corners


def calculate_price_part2(coords: list[tuple[int, int]]) -> int:
    corners = 0
    n = len(coords)
    for coord in coords:
        corners += count_corners(coords, coord)
    
    price = n * corners
    return price


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")

    grid = {}

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    
    current_char = None
    total_price = 0

    for coord, char in grid.items():
        if char == ".":
            continue
        to_check: list[tuple[int, int]] = []
        subgrid: list[tuple[int, int]] = []

        if not current_char:
            # We are starting a new subgrid
            current_char = char
            # to_check is our list of coordinates to check for neighbours
            to_check.append(coord)

            # subgrid is our variable to track all coords that belong to our subgrid
            subgrid.append(coord)

        while to_check:
            next_to_check = to_check.pop(0)
            potential_neighbours = get_neighbours(grid, next_to_check, char)
            for pn in potential_neighbours:
                if pn not in subgrid:
                    # Add the item to our subgrid
                    subgrid.append(pn)
                    # Also add the item to check for further neighbours
                    to_check.append(pn)
        current_char = None
        total_price += calculate_price_part1(subgrid)
        cleanse_grid(grid, subgrid)

    return str(total_price)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")

    grid = {}

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    
    current_char = None
    total_price = 0

    for coord, char in grid.items():
        if char == ".":
            continue
        to_check: list[tuple[int, int]] = []
        subgrid: list[tuple[int, int]] = []

        if not current_char:
            # We are starting a new subgrid
            current_char = char
            # to_check is our list of coordinates to check for neighbours
            to_check.append(coord)

            # subgrid is our variable to track all coords that belong to our subgrid
            subgrid.append(coord)

        while to_check:
            next_to_check = to_check.pop(0)
            potential_neighbours = get_neighbours(grid, next_to_check, char)
            for pn in potential_neighbours:
                if pn not in subgrid:
                    # Add the item to our subgrid
                    subgrid.append(pn)
                    # Also add the item to check for further neighbours
                    to_check.append(pn)
        current_char = None
        total_price += calculate_price_part2(subgrid)
        cleanse_grid(grid, subgrid)

    return str(total_price)

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
