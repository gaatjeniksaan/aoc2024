from collections import defaultdict
from pathlib import Path
from typing import Final


DAY: Final[int] = 5
YEAR: Final[int] = 2024


def main():
    solution1 = part1()
    print(f"solution for part1: {solution1}")
    # aocd.submit(solution1, part="a", day=DAY, year=YEAR)

    solution2 = part2()
    print(f"solution for part2: {solution2}")
    # aocd.submit(solution2, part="b", day=DAY, year=YEAR)


def part1(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    data, checks = data.split("\n\n")
    data = data.split("\n")
    checks = checks.split("\n")
    cleaned_checks = []
    for c in checks:
        cleaned_checks.append(c.split(","))

    dd = defaultdict(list)
    dd_rev = defaultdict(list)

    for d in data:
        before, after = d.split("|")

        dd[before].append(after)
        dd_rev[after].append(before)


    valid_checks = []
    for check in cleaned_checks:
        valid = True
        for i, item in enumerate(check):
            rest = check[i+1::]
            followers = dd[item]
            for r in rest:
                if r not in followers:
                    valid = False
       
        if valid:
            valid_checks.append(check)
    
    answer = 0
    for vc in valid_checks:
        answer += int(vc[len(vc)//2])

    return answer


def part2(sample_input: bool = False) -> str:
    data = load_data(sample_input)

    data, checks = data.split("\n\n")
    data = data.split("\n")
    checks = checks.split("\n")
    cleaned_checks = []
    for c in checks:
        cleaned_checks.append(c.split(","))

    dd = defaultdict(list)
    dd_rev = defaultdict(list)

    for d in data:
        before, after = d.split("|")
        dd[before].append(after)
        dd_rev[after].append(before)

    invalid_checks = []
    for check in cleaned_checks:
        valid = True
        for i, item in enumerate(check):
            rest = check[i+1::]
            followers = dd[item]
            for r in rest:
                if r not in followers:
                    valid = False
        if not valid:
            invalid_checks.append(check)

    sorted_checks = []
    for check in invalid_checks:   
        sorted_check = []
        remaining = check.copy()
            
        while remaining:
            for item in remaining:
                has_predecessor = False
                for other in remaining:
                    if other != item and item in dd[other]:
                        has_predecessor = True
                        break
                
                if not has_predecessor:
                    sorted_check.append(item)
                    remaining.remove(item)
                    break
        
        sorted_checks.append(sorted_check)
    
    answer = 0
    for vc in valid_checks:
        answer += int(vc[len(vc)//2])

    return answer


def load_data(sample_input: bool) -> str:
    p = Path(__file__).parent.absolute()
    
    data_path = p / "input.txt" if not sample_input else p / "tests" / "example.txt"
    
    return data_path.read_text()


if __name__ == "__main__":
    main()
