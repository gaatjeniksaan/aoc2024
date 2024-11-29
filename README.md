# aoc2024

## Requirements

1. uv
2. your AoC Session cookie saved under `~/.config/aocd/token`, see https://github.com/wimglenn/advent-of-code-wim/issues/1 for details

Advent of Code 2024 blueprint for your 2024 entries.

```bash
uv run setup_day.py -d 12 -e "<ANSWER-TO-THE-EXAMPLE-CALCULATION>"
```

This will create a blueprint for day `12`:

1. create a folder `/day12`
2. create a `main.py` file for you to populate with your logic
3. download your input data and put it under `/day12/input.txt`
4. create a folder `/day12/tests` with a `test_day12.py` file
5. you can populate `example.txt` yourself with input from the example
    a. this will be used to assert against

If you are happy with your solution, you can run to test against the example data:

```bash
uv run pytest ./day12
```

If that passes, you can uncomment the `submit` lines for solution part1 and part2 to actually submit.
