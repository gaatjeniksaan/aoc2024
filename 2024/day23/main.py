from collections import defaultdict
from pathlib import Path
import time
from typing import Final

import aocd
import networkx


EXAMPLE_ANSWER_1: Final[str] = "7"
EXAMPLE_ANSWER_2: Final[str] = "co,de,ka,ta"
DAY: Final[int] = 23
YEAR: Final[int] = 2024


def main():
    answer1 = part1(sample_input=True)
    assert answer1 == EXAMPLE_ANSWER_1, f"calculated answer '{answer1}' != expected answer '{EXAMPLE_ANSWER_1}'"
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


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")

    conns = defaultdict(list)
    sets = set()

    for conn in data:
        l, r = conn.split("-")
        conns[l].append(r)
        conns[r].append(l)
    
    for conn in data:
        l, r = conn.split("-")
        l_conns = conns[l]
        r_conns = conns[r]
        for lc in l_conns:
            if lc in r_conns:
                combo = sorted([l, r, lc])
                sets.add(tuple(combo))
        # for rc in r_conns:
        #     if rc in l_conns:
        #         combo = sorted([l, r, rc])
        #         sets.add(tuple(combo))
    total = 0
    for s in sets:
        if any(x.startswith("t") for x in s):
            total += 1

    return str(total)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")

    g = networkx.Graph()
    for conn in data:
        t = tuple(conn.split("-"))
        g.add_edges_from([t])

    longest = []
    for x in networkx.find_cliques(g):
        if len(x) > len(longest):
            longest = x
    print(",".join(sorted(longest)))

    answer = ",".join(sorted(longest))
    return answer
 


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
