import re
from pathlib import Path
from typing import Final


DAY: Final[int] = 3
YEAR: Final[int] = 2024


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> int:
    data = load_data(sample_input)

    pattern = r"mul\(\d{1,3},\d{1,3}\)"

    matches = re.findall(pattern, data)

    items = [item.split(",") for item in matches]

    total = 0
    for item in items:
        l = item[0].lstrip("mul(")
        r = item[1].rstrip(")")

        total += int(l) * int(r)

    # So we only want the parts where we see mul(xxx,yyy)

    # Your implementation goes here
    return total


def part2(sample_input: bool = False) -> int:
    data = load_data(sample_input)

    enabled = True
    parts: list[str] = []

    for i, char in enumerate(data):
        if enabled:
            parts.append(char)
        do = data[i:i+4]
        dont = data[i:i+7]

        if do == "do()":
            enabled = True
        if dont == "don't()":
            enabled = False

    cleaned_data = "".join(parts)

    pattern = r"mul\(\d{1,3},\d{1,3}\)"

    matches = re.findall(pattern, cleaned_data)

    items = [item.split(",") for item in matches]

    total = 0
    for item in items:
        l = item[0].lstrip("mul(")
        r = item[1].rstrip(")")

        total += int(l) * int(r)

    return total


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
