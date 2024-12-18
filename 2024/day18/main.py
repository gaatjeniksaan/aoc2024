import heapq
import itertools
from pathlib import Path
import time
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "22"
EXAMPLE_ANSWER_2: Final[str] = "NO ANSWER PROVIDED"  # Provide this yourself
DAY: Final[int] = 18
YEAR: Final[int] = 2024


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

    answer2 = part2(sample_input=True) == EXAMPLE_ANSWER_2
    assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    start = (0, 0)
    end = (70, 70)
    n_bytes = 2974
    grid_coords = itertools.product(range(end[0] + 1), range(end[1] + 1))
    grid = {(coord[0], coord[1]): "." for coord in grid_coords}
    last = (0, 0)
    for n, line in enumerate(data.split("\n")):
        if n >= n_bytes:
            break
        coord = line.split(",")
        # print(f"{coord=}")
        grid[(int(coord[0]), int(coord[1]))] = "#"
        last = (int(coord[0]), int(coord[1]))
        
    # Our queue takes a list of tuples containing:
    # the steps / (x, y)
    queue: list[tuple[int, tuple[int, int]]] = []
    
    direction_mapper = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    # for y in range(end[1]+1):
    #     line = []
    #     for x in range(end[0]+1):
    #         line.append(grid[(x, y)])
    #     print("".join(line))
    
    # We push onto the queue: a tuple with cost / current coord (x,y) / direction str
    # The reindeer starts facing East.
    heapq.heappush(queue, (0, start))
    visited: list[tuple[int, int]] = []

    while queue:
        steps, coord = heapq.heappop(queue)

        if coord == end:
            print(f"Reached the end baby!! {steps=}")
            raise ValueError(f"success for {n_bytes=}:{last=}")
            return str(steps)
        
        if coord in visited:
            continue

        visited.append(coord)

        for dir in direction_mapper.values():
            x = coord[0] + dir[0]
            y = coord[1] + dir[1]
            new_coord = (x, y)
            
            char = grid.get(new_coord)
            # print(f"'{char}':{new_coord=}")
            if char == "#":
                # print(f"found # for {new_coord}")
                continue
            if char is None:
                continue            
            if new_coord in visited:
                continue
            # print(f"pushing {coord}:{steps}->{new_coord}:{steps+1}")
            heapq.heappush(queue, (steps + 1, new_coord))
    raise ValueError(f"{last=}")
    return len(visited)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    
    # Your implementation goes here
    answer = "geenidee"
    return answer
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
