from collections import defaultdict
import heapq
import time
from pathlib import Path
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "11048"
EXAMPLE_ANSWER_2: Final[str] = "11048"  # Provide this yourself
DAY: Final[int] = 16
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

    answer2 = part2(sample_input=False) == EXAMPLE_ANSWER_2
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def get_2d_grid(data: str) -> dict[tuple[int, int], str]:
    grid = {}
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    
    return grid


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    start = (0, 0)
    end = (0, 0)
    grid = {}

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
            grid[(x, y)] = char

    # Our queue takes a list of tuples containing:
    # the cost / (x, y) / direction
    queue: list[tuple[int, tuple[int, int], str]] = []
    
    # Visited takes tuples containing:
    # (x, y) / direction
    visited: set[tuple[tuple[int, int], str]] = set()
    direction_mapper = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }
    turn_mapper = {
        "N": ["E", "W"],
        "E": ["N", "S"],
        "S": ["E", "W"],
        "W": ["N", "S"],
    }

    # We push onto the queue: a tuple with cost / current coord (x,y) / direction str
    # The reindeer starts facing East.
    heapq.heappush(queue, (0, start, "E"))

    while queue:
        cost, coord, direction = heapq.heappop(queue)
        print(f"{cost=}, {coord=}, {direction=}")

        if coord == end:
            print(f"Reached the end baby!! {cost=}")
            return str(cost)
        
        visit = (coord, direction)
        if visit in visited:
            continue

        visited.add(visit)

        # Forward step:
        dir_coord = direction_mapper[direction]
        forward_coord = (coord[0] + dir_coord[0], coord[1] + dir_coord[1])

        # Don't hit a wall!
        if grid[forward_coord] != "#":
            new_cost = cost + 1
            heapq.heappush(queue, (new_cost, forward_coord, direction))

        # Now check turns:
        turns = turn_mapper[direction]
        for turn in turns:
            new_cost = cost + 1000
            heapq.heappush(queue, (new_cost, coord, turn))


    # Your implementation goes here
    answer = "geenidee"
    return answer


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    start = (0, 0)
    end = (0, 0)
    grid = {}

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
            grid[(x, y)] = char

    # Our queue takes a list of tuples containing:
    # the cost / (x, y) / direction
    queue: list[tuple[int, tuple[int, int], str]] = []
    
    # Visited takes tuples containing:
    # (x, y) / direction
    visited: set[tuple[tuple[int, int], str]] = set()
    
    final_cost = 0
    final_direction = ""
    # Keep track of coordinates + direction their cheapest cost to get there.
    # Set unknown keys to some unrealistic value
    costs = {}

    direction_mapper = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    turn_mapper = {
        "N": ["E", "W"],
        "E": ["N", "S"],
        "S": ["E", "W"],
        "W": ["N", "S"],
    }

    # We push onto the queue: a tuple with cost / current coord (x,y) / direction str
    # The reindeer starts facing East.
    heapq.heappush(queue, (0, start, "E"))

    while queue:
        cost, coord, direction = heapq.heappop(queue)
        current_lowest_cost = costs.get((coord, direction))
        if not current_lowest_cost:
            costs[(coord, direction)] = cost
        else:
            costs[(coord, direction)] = min(cost, current_lowest_cost)
    
        if coord == end:
            final_cost = cost
            final_direction = direction
            break
        
        visit = (coord, direction)
        if visit in visited:
            continue

        visited.add(visit)

        # Forward step:
        dir_coord = direction_mapper[direction]
        forward_coord = (coord[0] + dir_coord[0], coord[1] + dir_coord[1])

        # Don't hit a wall!
        if grid[forward_coord] != "#":
            new_cost = cost + 1
            heapq.heappush(queue, (new_cost, forward_coord, direction))

        # Now check turns:
        turns = turn_mapper[direction]
        for turn in turns:
            new_cost = cost + 1000
            heapq.heappush(queue, (new_cost, coord, turn))

    # So we've reached the end, now we need to backtrack and count locations travelled.
    locations: set[tuple[int, int]] = set([end])

    # We backtrack by adding items to it like so:
    # cost / (x, y) / direction
    backtrack_queue: list[tuple[int, tuple[int, int], str]] = []
    heapq.heappush(backtrack_queue, (final_cost, end, final_direction))

    while backtrack_queue:
        cost, coord, direction = heapq.heappop(backtrack_queue)
        print(f"{cost=}, {coord=}, {direction=}")
        # Log locations, will turn into a set later.
        locations.add(coord)

        dir_coord = direction_mapper[direction]

        new_coord = (coord[0] - dir_coord[0], coord[1] - dir_coord[1])

        new_cost = costs.get((new_coord, direction))
        
        # Check if the next normal step is present
        if new_cost:
            if new_cost < cost:
                heapq.heappush(backtrack_queue, (new_cost, new_coord, direction))
        
        # Check if turns are present and cheaper:
        turns = turn_mapper[direction]
        for turn in turns:
            new_cost = costs.get((coord, turn))
            print(f"{coord=}:{coord=}\t{turn=}:{new_cost=}\t{turns=}")
            print(f"{new_cost=} for {turn=}")
            if not new_cost:
                continue
            if new_cost < cost:
                heapq.heappush(backtrack_queue, (new_cost, coord, turn))


    # Your implementation goes here
    for y in range(141):
            line = ""
            for x in range(141):
                if (x, y) in locations:
                    line += "O"
                else:
                    line += grid[(x, y)]
            print(line)
    raise ValueError(len(set(locations)))
    # return len(locations)

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
