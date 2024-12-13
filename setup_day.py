import argparse
import pathlib
from typing import Final

from aocd.models import Puzzle


YEAR: Final[int] = 2024


def main(day: int, year: int, example: str) -> None:
    print(f"setting up for {day=}")

    root_dir = pathlib.Path().absolute()

    day_dir = root_dir / str(year) / f"day{day}"

    # Set exist_ok = False, so we fail if we try to overwrite our
    day_dir.mkdir(parents=True, exist_ok=False)

    (day_dir / "example.txt").touch()

    # Copy solution template -> main.py
    with open(str(root_dir / "template_for_solution.py")) as source:
        content = source.read()
        modified_content = content.replace('1  # This will be regex/replaced', str(day))
        modified_content = modified_content.replace('"NO ANSWER PROVIDED"  # This will be replaced', f'"{example}"')

        with open(str(day_dir / "main.py"), "w") as target:
            target.write(modified_content)

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
