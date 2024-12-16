import time
import numpy as np
from collections import defaultdict
import functools
import time
from pathlib import Path
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "12"
EXAMPLE_ANSWER_2: Final[str] = "NO ANSWER PROVIDED"  # Provide this yourself
DAY: Final[int] = 14
YEAR: Final[int] = 2024


class Robot:
    def __init__(self, input: str):
        input_list = input.split(" ")
        self.x = int(input_list[0].split(",")[0].lstrip("p="))
        self.y = int(input_list[0].split(",")[1].lstrip("p="))
        self.vx = int(input_list[1].split(",")[0].lstrip("v="))
        self.vy = int(input_list[1].split(",")[1].lstrip("v="))
        return

    def move(self, max_x: int, max_y: int, n: int) -> None:
        x = self.x + self.vx * n
        y = self.y + self.vy * n

        self.x = x % max_x
        self.y = y % max_y
        # print(f"new coords: {self}")
        return

    def __str__(self) -> str:
        return f"Robot({self.x=}, {self.y=}, {self.vx=}, {self.vy=})"


def calculate_quadrants(robots: list[Robot], max_x: int, max_y: int) -> list[int]:
    quadrants = defaultdict(int)
    x_thres = max_x // 2
    y_thres = max_y // 2
    # print(f"{x_thres=}, {y_thres=}")
    for robot in robots:
        if robot.x == x_thres:
            print(f"skipping {str(robot)} because {robot.x=}")
            continue
        if robot.y == y_thres:
            print(f"skipping {str(robot)} because {robot.y=}")
            continue
    
        if robot.x < x_thres:
            if robot.y < y_thres:
                quadrants[1] += 1
                print(f"putting robot {str(robot)} in quadrant 1")
            else:
                print(f"putting robot {str(robot)} in quadrant 3")
                quadrants[3] += 1
        
        else:
            if robot.y < y_thres:
                print(f"putting robot {str(robot)} in quadrant 2")
                quadrants[2] += 1
            else:
                print(f"putting robot {str(robot)} in quadrant 4")
                quadrants[4] += 1
        

    print(f"{quadrants=}")
    return [v for v in quadrants.values()]


def is_symmetry(grid: dict[tuple[int, int], bool], max_x: int) -> bool:
    middle_x = max_x // 2

    for coord in grid:
        x = coord[0]
        if x >= middle_x:
            continue
        
        y = coord[1]
        pair_x = middle_x + middle_x - x
        pair = (pair_x, y)
        if pair not in grid:
            return False

    return True


def main():
    # answer1 = part1(sample_input=True)
    # assert answer1 == EXAMPLE_ANSWER_1, f"calculated answer '{answer1}' != expected answer '{EXAMPLE_ANSWER_1}'"
    start_time = time.time()
    solution1 = part1()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part1: {solution1}")
    print(f"Execution time for part1: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    # answer2 = part2(sample_input=True) == EXAMPLE_ANSWER_2
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")
    robots: list[Robot] = []
    for d in data:
        robots.append(Robot(d))
    
    max_x = 101
    max_y = 103
    n = 100
    print([str(r) for r in robots])
    for r in robots:
        r.move(max_x, max_y, n)
        # moved_robots.append(move_robot(r, max_x, max_y, 1))
    
    print(f"AFTER {n=} SECONDS")

    for r in robots:
        print(str(r))
    quadrants = calculate_quadrants(robots, max_x, max_y)
    print(f"{quadrants=}")
    sf = functools.reduce(lambda x, y: x * y, quadrants, 1)

    # Your implementation goes here
    return str(sf)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")
    robots: list[Robot] = []
    for d in data:
        robots.append(Robot(d))
    
    max_x = 101
    max_y = 103
    n = 0
    print([str(r) for r in robots])
    vars = []
    while n < 10001:
        n += 1
        positions = defaultdict(list)
        pos = {}
        for r in robots:
            r.move(max_x, max_y, 1)
            pos[(r.x, r.y)] = True
        for robot in robots:
            positions[robot.y].append((robot.x))
        
        var = get_variance(positions)
        vars.append((var, n))

        if n >= 6470:
            print("========================================")
            print(f"{n=}")
            print_grid(pos)            
            print("========================================")
            if n == 6475:
                raise ValueError("got it")


        # print(f"{n=}\t{var=}")
    
    v = sorted(vars, key=lambda x: x[0])

    raise ValueError(f"{v[:10]}")
 

def get_variance(positions: dict[int, list[int]]) -> float:
    averages = []
    for y, xs in positions.items():
        avg = sum(xs) / len(xs)
        averages.append(avg)
    
    return float(np.var(averages))


def print_grid(positions: dict[int, bool]) -> None:
    for y in range(0, 103):
        for x in range(0, 101):
            if (x, y) in positions:
                print("X", end="")
            else:
                print(" ", end="")
        print()
    print("\n\n")



def is_symmetrical(positions: dict[int, list[int]]) -> bool:
    current_symmetry = None
    for values in positions.values():
        sym = int(sum(values) / len(values))
        if not current_symmetry:
            current_symmetry = sym
            continue

        if not sym == current_symmetry:
            return False
    return True


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
