from functools import cache
import heapq
from pathlib import Path
import time
from typing import Final

import aocd


EXAMPLE_ANSWER_1: Final[str] = "126384"
EXAMPLE_ANSWER_2: Final[str] = "NO ANSWER PROVIDED"  # Provide this yourself
DAY: Final[int] = 21
YEAR: Final[int] = 2024


mapper = {
    # Key is from character -> to character
    # So A< means, robot is @ A and want to go to <

    # First the directional robots
    "A<": "v<<A",
    "Av": "<vA",
    "A>": "vA",
    "A^": "<A",
    "AA": "A",

    "<v": ">A",
    "<>": ">>A",
    "<^": ">^A",
    "<A": ">>^A",
    "<<": "A",

    "v<": "<A",
    "v^": "^A",
    "v>": ">A",
    "vA": "^>A",
    "vv": "A",

    "^<": "v<A",
    "^v": "vA",
    "^A": ">A",
    "^>": "v>A",
    "^^": "A",

    ">A": "^A",
    ">v": "<A",
    "><": "<<A",
    ">^": "<^A",
    ">>": "A",

    # Now all the numeric ones...
    "AA": "A",
    "A0": "<A",
    "A1": "^<<A",
    "A2": "<^A",
    "A3": "^A",
    "A4": "^^<<A",
    "A5": "<^^A",
    "A6": "^^A",
    "A7": "^^^<<A",
    "A8": "^^^<A",
    "A9": "^^^A",

    "0A": ">A",
    "00": "A",
    "01": "^<A",
    "02": "^A",
    "03": "^>A",
    "04": "^^<A",
    "05": "^^A",
    "06": "^^>A",
    "07": "^^^<A",
    "08": "^^^A",
    "09": "^^^>A",

    "1A": ">>vA",
    "10": ">vA",
    "11": "A",
    "12": ">A",
    "13": ">>A",
    "14": "^A",
    "15": "^>A",
    "16": "^>>A",
    "17": "^^A",
    "18": "^^>A",
    "19": "^^>>A",

    "2A": "v>A",
    "20": "vA",
    "21": "<A",
    "22": "A",
    "23": ">A",
    "24": "<^A",
    "25": "^A",
    "26": "^>A",
    "27": "^^<A",
    "28": "^^A",
    "29": "^^>A",

    "3A": "vA",
    "30": "<vA",
    "31": "<<A",
    "32": "<A",
    "33": "A",
    "34": "<<^A",
    "35": "<^A",
    "36": "^A",
    "37": "<<^^A",
    "38": "<^^A",
    "39": "^^A",

    "40": ">vvA",
    "4A": ">>vvA",
    "41": "vA",
    "42": "v>A",
    "43": ">>vA",
    "44": "A",
    "45": ">A",
    "46": ">>A",
    "47": "^A",
    "48": "^>A",
    "49": "^>>A",

    "5A": ">vvA",
    "50": "vvA",
    "51": "<vA",
    "52": "vA",
    "53": "v>A",
    "54": "<A",
    "55": "A",
    "56": ">A",
    "57": "<^A",
    "58": "^A",
    "59": "^>A",

    "6A": "vvA",
    "60": "vv<A",
    "61": "<<vA",
    "62": "<vA",
    "63": "vA",
    "64": "<<A",
    "65": "<A",
    "66": "A",
    "67": "<<^A",
    "68": "<^A",
    "69": "^A",

    "7A": ">>vvvA",
    "70": ">vvvA",
    "71": "vvA",
    "72": "vv>A",
    "73": "vv>>A",
    "74": "vA",
    "75": "v>A",
    "76": "v>>A",
    "77": "A",
    "78": ">A",
    "79": ">>A",

    "8A": "vvv>A",
    "80": "vvvA",
    "81": "<vvA",
    "82": "vvA",
    "83": "vv>A",
    "84": "<vA",
    "85": "vA",
    "86": "v>A",
    "87": "<A",
    "88": "A",
    "89": ">A",

    "9A": "vvvA",
    "90": "<vvvA",
    "91": "<<vvA",
    "92": "<vvA",
    "93": "vvA",
    "94": "<<vA",
    "95": "<vA",
    "96": "vA",
    "97": "<<A",
    "98": "<A",
    "99": "A",
}


def get_n_moves() -> int:
    pass


def get_n_moves_for_pair() -> int:
    pass


@cache
def get_moves(current: str, target: str, level: int, depth: int) -> int:
    if level >= target:
        return 
    
    print(f"{level=}")
    new_moves = move(code)
    return get_moves(new_moves, level + 1, target=target)


@cache
def move(moves: str) -> str:
    start = "A"
    total_moves = ""

    for move in moves:
        new_moves = mapper[start + move]
        total_moves += new_moves
        start = move

    return total_moves


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

    # answer2 = part2(sample_input=True)
    # assert answer2 == EXAMPLE_ANSWER_2, f"calculated answer '{answer2}' != expected answer '{EXAMPLE_ANSWER_2}'"
    start_time = time.time()
    solution2 = part2()
    end_time = time.time()

    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"solution for part2: {solution2}")
    print(f"Execution time for part2: {elapsed_time_ms:.2f} ms")
    aocd.submit(solution2, part="b", day=DAY, year=YEAR)


# def part1(sample_input: bool = False) -> str:
#     data = load_data(sample_input).split("\n")
#     print(data)
#     answer = 0
#     for i, code in enumerate(data):
#         for _ in range(3):
#             new_moves = move(code)
#             code = new_moves
        
#         len_code = len(code)
#         original_code = data[i]
#         numerical = int(original_code.rstrip("A"))
#         answer += (len_code * numerical)
#         # answer.append(numerical * len_code)

#     # Your implementation goes here
#     return str(answer)


def part1(sample_input: bool = False):
    data = load_data(sample_input).split("\n")
    print(data)
    answer = 0
    for i, code in enumerate(data):
        old_time = time.time()
        n_moves = get_moves(code, 1, target=4)
        new_time = time.time()

        # print(f"{i}:{j} took: {(new_time - old_time)} s")

        # code = new_moves
        
        len_code = n_moves
        original_code = data[i]
        numerical = int(original_code.rstrip("A"))
        answer += (len_code * numerical)
        # answer.append(numerical * len_code)

    # Your implementation goes here
    return str(answer)


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input).split("\n")
    print(data)
    answer = 0
    for i, code in enumerate(data):
        old_time = time.time()
        new_moves = get_moves(code, 1, target=27)
        new_time = time.time()

        # print(f"{i}:{j} took: {(new_time - old_time)} s")

        code = new_moves
        
        len_code = len(code)
        original_code = data[i]
        numerical = int(original_code.rstrip("A"))
        answer += (len_code * numerical)
        # answer.append(numerical * len_code)

    # Your implementation goes here
    return str(answer)
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
