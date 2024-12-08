import itertools
from collections import defaultdict
from pathlib import Path
from typing import Final


DAY: Final[int] = 8
YEAR: Final[int] = 2024

# Max coordinates
X = 49
Y = 49


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def compute_antinodes(nodes: list[tuple[int, int]]):
    combinations = itertools.combinations(nodes, 2)
    for combo in combinations:

        mini = min(combo)
        maxi = max(combo)

        delta = (maxi[0] - mini[0], maxi[1] - mini[1])
        
        antinode1 = (mini[0] - delta[0], mini[1] - delta[1])
        antinode2 = (maxi[0] + delta[0], maxi[1] + delta[1])

        yield antinode1
        yield antinode2


def compute_antinodes_part2(nodes: list[tuple[int, int]]):
    combinations = itertools.combinations(nodes, 2)
    for combo in combinations:
        mini = min(combo)
        maxi = max(combo)
        yield mini
        yield maxi
        delta = (maxi[0] - mini[0], maxi[1] - mini[1])

        # Check antinodes in negative direction
        current = (mini[0] - delta[0], mini[1] - delta[1])
        while (0 <= current[0] <= X) and (0 <= current[1] <= Y):
            yield current
            current = (current[0] - delta[0], current[1] - delta[1])
        
        # Check antinodes in positive direction
        current = (maxi[0] + delta[0], maxi[1] + delta[1])
        while (0 <= current[0] <= X) and (0 <= current[1] <= Y):
            yield current
            current = (current[0] + delta[0], current[1] + delta[1])


def part1(sample_input: bool = False) -> bool:
    data = load_data(sample_input)
    lines = data.split("\n")
    grid = defaultdict(list)
    nodes = dict()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            nodes[(x, y)] = False
            if char == ".":
                continue
            grid[char].append((x,y))

    # Iterate over every unique character and check the locations it has
    for char, locations in grid.items():
        # Compute antinodes for list of node locations
        for antinode in compute_antinodes(locations):
            if antinode in nodes:
                nodes[antinode] = True
    
    return sum([x for x in nodes.values() if x is True])


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    lines = data.split("\n")
    grid = defaultdict(list)
    nodes = dict()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            nodes[(x, y)] = False
            if char == ".":
                continue
            grid[char].append((x,y))

    # Iterate over every unique character and check the locations it has
    for char, locations in grid.items():
        # Compute antinodes for list of node locations
        for antinode in compute_antinodes_part2(locations):
            if antinode in nodes:
                nodes[antinode] = True
    
    print(f"{[k for k, v in nodes.items() if v]}")
    return sum([x for x in nodes.values() if x is True])
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
