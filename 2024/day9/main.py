import itertools
from pathlib import Path
from typing import Final


DAY: Final[int] = 9
YEAR: Final[int] = 2024


def main():
    # solution1 = part1()
    # print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def lookbefore(array, char, pointer) -> bool:
    return array[pointer - 1] == char


def lookahead(array, i) -> bool:
    return array[i + 1] == "."


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)
    array, dot_locations, char_locations = create_array1(data)
    # print("".join(x for x in array))
    pointer = len(array) - 1

    # assume we don't hit a "." at the end...
    highest_id = int(array[pointer])

    while pointer > 0:
        # print(f"{pointer=}")
        block_f = pointer
        char = array[pointer]
        if char == ".":
            # print(f"found a '.' at {pointer=} in {array=}")
            pointer -= 1
            continue
        
        # If we are dealing with a character that is higher than where we are
        # we should skip it, since we've already seen it.
        if int(char) > int(highest_id):
            pointer -= 1
            continue
        
        # We are cooking with gas, so let's update our highest_id
        highest_id = int(char)

        # See how many items we have in a row
        while lookbefore(array, char, pointer):
            pointer -= 1
        block_s = pointer

        values_to_move = array[block_s:block_f + 1]
        n_values_to_move = len(values_to_move)
        # print(f"{values_to_move=}")

        # Time to find a free slot from the start
        start = 0
        free_s = 0
        free_f = 0
        while start < pointer:
            # print(f"{start=}, {pointer=}, {n_values_to_move=}")
            # If we are not at a ".", we should just hop to the next
            if array[start] != ".":
                start += 1
                continue
            
            free_s = start
            while lookahead(array, start):
                start += 1
            free_f = start
            # print(f"{free_s=}, {free_f=}")
            
            # If we have space to move, we can do that here
            if (1 + free_f - free_s) >= n_values_to_move:
                # print(f"array before: \n{"".join(x for x in array)}")
                # print(f"moving {values_to_move=} to [{free_s}:{free_f}]")
                array[free_s:(free_s + n_values_to_move)] = values_to_move
                array[block_s:block_f + 1] = ["." for _ in range(n_values_to_move)]
                # print(f"array after: \n{"".join(x for x in array)}")
                break
            
            start += 1
        pointer -= 1
    # print(f"final {array=}")

    total = 0
    for i, value in enumerate(array):
        if value == ".":
            continue
        total += i * int(value)

    return total


def create_array1(data: str):
    dot = "."
    id_ = 0
    array = []
    dot_locations = []
    char_locations = []
    for i, char in enumerate(data):
        n = int(char)
        if i % 2 == 0:
            array.extend([str(id_) for _ in range(n)])
            id_ += 1
        else:
            array.extend([dot for _ in range(n)])

    for i, char in enumerate(array):
        if char == ".":
            dot_locations.append(i)
        else:
            char_locations.append(i)
    # print(dot_locations)
    char_locations = sorted(char_locations)
    return array, dot_locations, char_locations


def part1(sample_input: bool = True) -> str:
    data = load_data(sample_input)
    array, dot_locations, char_locations = create_array1(data)
    last_index = char_locations[-1]
    for i in dot_locations:
        print("".join(x for x in array))
        if i >= last_index:
            break
        index = char_locations.pop()
        item = array[index]
        # print(f"{index=}, {item=}")
        array[index] = "."
        array[i] = item
        last_index = index

    # print(array)
    # Your implementation goes here
    sorted_array = [int(x) for x in array if x != "."]

    total = 0
    for i, value in enumerate(sorted_array):
        total += i * value

    return total
 

def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
