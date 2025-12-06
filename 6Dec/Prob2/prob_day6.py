from __future__ import annotations

import os
from typing import List


def read_worksheet(path: str) -> List[str]:
    """
    Read the worksheet from input file.
    
    Args:
        path: Path to input file
        
    Returns:
        List of lines from the worksheet
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    return lines


def parse_problems_right_to_left(lines: List[str]) -> List[tuple]:
    """
    Parse problems using the same logic as the working NumPy code.
    Each column is either:
      - a digit (part of a number)
      - or pure whitespace (separator)
    """

    if not lines:
        return []

    # All lines except the last contain the vertical numbers
    data_lines = lines[:-1]

    # Last line contains operators separated by spaces
    operations = [x for x in lines[-1].split(" ") if x != ""]

    # Convert into a 2D list (preserving spacing)
    max_len = max(len(line) for line in data_lines)
    grid = [list(line.ljust(max_len)) for line in data_lines]

    # Transpose columns
    columns = ["".join(row[c] for row in grid) for c in range(max_len)]

    # Group columns into problems
    groups = []
    current_group = []

    for col in columns:
        if col.isspace():      # separator column
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(col)

    if current_group:
        groups.append(current_group)

    # Now groups[i] corresponds to operations[i]
    problems = []
    for idx, op in enumerate(operations):
        nums = [int(v) for v in groups[idx]]
        problems.append((nums, op))

    return problems


def solve_problem(numbers: List[int], operator: str) -> int:
    """
    Solve a single problem by applying the operator to all numbers.
    
    Args:
        numbers: List of numbers in the problem
        operator: Either '+' or '*'
        
    Returns:
        Result of applying the operator to all numbers
    """
    if not numbers:
        return 0
    
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Unknown operator: {operator}")


def calculate_grand_total(problems: List[tuple]) -> int:
    """
    Calculate the grand total by summing all problem answers.
    
    Args:
        problems: List of (numbers, operator) tuples
        
    Returns:
        Grand total (sum of all problem answers)
    """
    total = 0
    for numbers, operator in problems:
        answer = solve_problem(numbers, operator)
        total += answer
    return total


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    lines = read_worksheet(input_path)
    problems = parse_problems_right_to_left(lines)
    result = calculate_grand_total(problems)
    print(result)


if __name__ == "__main__":
    main()

