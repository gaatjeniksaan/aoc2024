import functools
import itertools
import operator
from pathlib import Path
from typing import Final


DAY: Final[int] = 7
YEAR: Final[int] = 2024


def main():
    solution1, unsuccesful = part1(True)
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2(unsuccesful)
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def generate_combinations(l1, ops):
    combos = list(itertools.product(ops, repeat=len(l1)))
    for combo in combos:
        current = []
        for op, num in zip(combo, l1):
            # print(op, num)
            current.append((op, num))
        yield current


def apply_operator(accumulator, op_and_val):
    operator, value = op_and_val
    return operator(accumulator, value)


def reducer(l):
   
    total = 1
    for op, value in l:
        total = op(total, value)
    return total


def concat(a, b):
    return int(str(a) + str(b))


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    lines = data.split("\n")
    l2 = [v.split(":") for v in lines]
    final = {int(v[0]): list(map(int, v[1].lstrip().split())) for v in l2}
    ops = [operator.add, operator.mul]
    total = 0
    unsuccessful = {}
    
    for v, l in final.items():
        for c in generate_combinations(l, ops):
            result = reducer(c)
            if result == v:
                total += int(v)
                break
        
        unsuccessful[v] = l

    # Your implementation goes here
    
    return total, unsuccessful


def part2(unsuccessful: dict) -> str:
    final = unsuccessful
    ops = [operator.add, operator.mul, concat]
    total = 0
    
    for v, l in final.items():
        for c in generate_combinations(l, ops):
            result = functools.reduce(apply_operator, c[1:], c[0][1])
            # print(result)
            if result == v:
                total += int(v)
                break

    # Your implementation goes here
    
    return total 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
