import argparse
import pathlib
from typing import Final

from aocd.models import Puzzle


YEAR: Final[int] = 2024


def main(day: int, year: int, example: str) -> None:
    print(f"setting up for {day=}")

    root_dir = pathlib.Path().absolute()

    day_dir = root_dir / str(year) / f"day{day}"

    test_dir = day_dir / "tests" 
    # Set exist_ok = False, so we fail if we try to overwrite our
    test_dir.mkdir(parents=True, exist_ok=False)

    test_example_data = test_dir / "example.txt"
    test_example_data.touch()

    # Copy solution template -> main.py
    with open(str(root_dir / "template_for_solution.py")) as source:
        content = source.read()
        modified_content = content.replace('1  # This will be regex/replaced', str(day))

        with open(str(day_dir / "main.py"), "w") as target:
            target.write(modified_content)

    # Copy test template -> tests/test_dayx.py
    with open(str(root_dir / "template_for_test.py")) as source:
        content = source.read()
        modified_content = content.replace('""  # This will be replaced with input from user', f'"{example}"')

        with open(str(test_dir / f"test_day{day}.py"), "w") as target:
            target.write(modified_content)
        
    # Populate /tests with __init__.py
    (test_dir / "__init__.py").touch()

    # Populate puzzle input
    puzzle = Puzzle(year=year, day=day)
    
    input_txt_file = day_dir / "input.txt"
    input_txt_file.write_text(puzzle.input_data)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser("aoc")
    argparser.add_argument("-d", "--day", type=int, help="Day number you want to init for.")
    argparser.add_argument("-y", "--year", default=YEAR, type=int, help=f"Year you wanna init for. Defaults to {YEAR=}")
    argparser.add_argument(
        "-e",
        "--example",
        type=str,
        default="NO EXAMPLE ANSWER PROVIDED",
        help="The answer of the example given, will be used to assert tests.",
    )
    args = argparser.parse_args()

    main(args.day, args.year, args.example)
