from typing import Final

from main import part1, part2


EXPECTED_ANSWER: Final[str] = 2


def test_part1():
    answer = part1(sample_input=True)
    assert EXPECTED_ANSWER == answer


def test_part2():
    answer = part2(sample_input=True)
    assert 4 == answer
