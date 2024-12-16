import re
import time
from pathlib import Path
from typing import Final

import aocd
import numpy as np


EXAMPLE_ANSWER_1: Final[str] = "480"
EXAMPLE_ANSWER_2: Final[str] = "NO ANSWER PROVIDED"  # Provide this yourself
DAY: Final[int] = 13
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

    # answer2 = part2(sample_input=True) == EXAMPLE_ANSWER_2
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def is_whole(n: float) -> bool:
    return not n % 1 == 0


def solve_equation(equation: dict[str, int | tuple[int, int]]) -> int:
    x_coeff = [equation["A"][0], equation["B"][0]]
    y_coeff = [equation["A"][1], equation["B"][1]]
    
    equations = np.array([x_coeff, y_coeff])
    sol = np.array([equation["X"], equation["Y"]])

    answer = np.linalg.solve(equations, sol)
    print(f"{answer=}")
    
    # if not all(is_whole(a) for a in answer):
    #     return 0
    
    a = round(answer[0])
    b = round(answer[1])

    aX = equation["A"][0]
    bX = equation["B"][0]
    aY = equation["A"][1]
    bY = equation["B"][1]
    pX = equation["X"]
    pY = equation["Y"]

    if a * aX + b * bX == pX and a * aY + b * bY == pY:
        solve = 3 * a + b
        print(f"solved! for {a, b}: {solve=}")
        return solve
        
    return 0
    return 3 * int(answer[0]) + int(answer[1])


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n\n")
    equation_sets = []
    
    for group in data:
        equation = {}
        
        for i, line in enumerate(group.split("\n")):
            if i == 0:
                x = re.findall(r'X\+(\d+)', line)
                y = re.findall(r'Y\+(\d+)', line)
                equation["A"] = (int(x[0]), int(y[0]))
            elif i == 1:
                x = re.findall(r'X\+(\d+)', line)
                y = re.findall(r'Y\+(\d+)', line)
                equation["B"] = (int(x[0]), int(y[0]))
            else:
                X = re.findall(r'X=+(\d+)', line)
                Y = re.findall(r'Y=+(\d+)', line)
                equation["X"] = int(X[0])
                equation["Y"] = int(Y[0])
        equation_sets.append(equation)        
    # Your implementation goes here

    total = 0
    for eq in equation_sets:
        cost = solve_equation(eq)
        total += cost
    
    print(f"TOTAL: {total}")

    return str(int(total))


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n\n")
    equation_sets = []
    
    for group in data:
        equation = {}
        
        for i, line in enumerate(group.split("\n")):
            if i == 0:
                x = re.findall(r'X\+(\d+)', line)
                y = re.findall(r'Y\+(\d+)', line)
                equation["A"] = (int(x[0]), int(y[0]))
            elif i == 1:
                x = re.findall(r'X\+(\d+)', line)
                y = re.findall(r'Y\+(\d+)', line)
                equation["B"] = (int(x[0]), int(y[0]))
            else:
                X = re.findall(r'X=+(\d+)', line)
                Y = re.findall(r'Y=+(\d+)', line)
                equation["X"] = int(X[0]) + 10000000000000
                equation["Y"] = int(Y[0]) + 10000000000000
        equation_sets.append(equation)        

    total = 0
    for eq in equation_sets:
        cost = solve_equation(eq)
        total += cost

    return str(int(total)) 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
