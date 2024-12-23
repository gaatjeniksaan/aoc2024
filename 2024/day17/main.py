from atexit import register
from collections import defaultdict
import itertools
from mimetypes import init
import multiprocessing
from pathlib import Path
import time
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "4,6,3,5,6,3,5,2,1,0"
EXAMPLE_ANSWER_2: Final[str] = "NO ANSWER PROVIDED"  # Provide this yourself
DAY: Final[int] = 17
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

    # elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    # print(f"solution for part2: {solution2}")
    # print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def get_combo_operand_value(operand: int, registers: dict[str, int]) -> int:
    if operand <= 3:
        return operand

    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    raise ValueError(f"wrong operand received: {operand}")


def adv(operand: int, registers: dict[str, int]) -> None:
    combo_op = get_combo_operand_value(operand, registers)
    num = registers["A"]
    denom = 2 ** combo_op
    registers["A"] = num // denom
    return


def bxl(operand: int, registers: dict[str, int]) -> None:
    num = registers["B"]
    registers["B"] = num ^ operand


def bst(operand: int, registers: dict[str, int]) -> None:
    combo_op = get_combo_operand_value(operand, registers)
    mask = (1 << 3) - 1
    val = combo_op % 8
    registers["B"] = val & mask
    return 


def jnz(operand: int, registers: dict[str, int]) -> int | None:
    a = registers["A"]
    if a == 0:
        return None
    return operand


def bxc(registers: dict[str, int]) -> None:
    b = registers["B"]
    c = registers["C"]
    registers["B"] = b ^ c
    return


def out(operand: int, registers: dict[str, int]) -> int:
    combo_op = get_combo_operand_value(operand, registers)
    return combo_op % 8


def bdv(operand: int, registers: dict[str, int]) -> None:
    combo_op = get_combo_operand_value(operand, registers)
    num = registers["A"]
    denom = 2 ** combo_op
    registers["B"] = num // denom
    return


def cdv(operand: int, registers: dict[str, int]) -> None:
    combo_op = get_combo_operand_value(operand, registers)
    num = registers["A"]
    denom = 2 ** combo_op
    registers["C"] = num // denom
    return


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    registers = {}
    program = []
    for line in data.split("\n"):
        if "Register" in line:
            line = line.lstrip("Register ").split(": ")
            registers[line[0]] = int(line[1])
        elif "Program" in line:
            line = line.lstrip("Program: ")
            for i in range(len(line)):
                if i % 2 == 0:
                    char = line[i]
                    program.append(int(char))
        else:
            continue
    i: int = 0
    output: str = ""

    while True:
        opcode = program[i]
        operand = program[i + 1]
        match opcode:
            case 0:
                adv(operand, registers)
            case 1:
                bxl(operand, registers)
            case 2:
                bst(operand, registers)
            case 3:
                val = jnz(operand, registers)
                if val is None:
                    break
                i = val
                continue
            case 4:
                bxc(registers)
            case 5:
                val = out(operand, registers)
                output += f"{val},"
            case 6:
                bdv(operand, registers)
            case 7:
                cdv(operand, registers)
        
        i += 2

    
    # Your implementation goes here
    return output.rstrip(",")


def run_program(initial_A: int, program: list[int], program_str: str) -> list[str]:
    i: int = 0
    running = True
    registers = {"A": initial_A, "B": 0, "C": 0}
    output: list[int] = []

    while True:
        opcode: int = program[i]
        operand: int = program[i + 1]

        match opcode:
            case 0:
                adv(operand, registers)
            case 1:
                bxl(operand, registers)
            case 2:
                bst(operand, registers)
            case 3:
                val = jnz(operand, registers)
                if val is None:
                    # output = output.rstrip(",")
                    # if len(output) == 31:
                    #     print(f"{initial_A}\t{len(output)=}\t\t{output=}")
                    #     raise ValueError(f"oops")
                    break
                i = val
                continue
            case 4:
                bxc(registers)
            case 5:
                val = out(operand, registers)
                output.append(val)
                # if not program_str.startswith(output):
                #     print(f"{initial_A=}\t\t{output=}")
                #     break
                # if output.rstrip(",") == program_str:
                #     raise ValueError(f"stopped for initial_A: {initial_A}, {output=}, {program_str=}")

            case 6:
                bdv(operand, registers)
            case 7:
                cdv(operand, registers)
            case _:
                raise ValueError("oopsie")
        i += 2

    return output


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    registers = {}
    program = []
    program_str: str = ""
    for line in data.split("\n"):
        if "Program" in line:
            line = line.lstrip("Program: ")
            program_str = line
            for i in range(len(line)):
                if i % 2 == 0:
                    char = line[i]
                    program.append(int(char))
        else:
            continue

    n = 16
    lengths = defaultdict(list)
    start =  190384113204000

    for initial_A in itertools.count(start=start, step=1):
        output = run_program(initial_A, program, program_str)
        print(f"{initial_A=}")
        print(f"{output=}")
        print()
        if output == program:
            raise ValueError(f"HALLELULAJ {initial_A}:{output=}:{program=}")
        if output[-n:] == program[-n:]:
            raise ValueError(f"initial_A found!! {initial_A}")

    raise ValueError(f"oops")



    
    
    
    # Your implementation goes here
    raise ValueError("oops")
    answer = "geenidee"
    return answer
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
