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


def parse_problems(lines: List[str]) -> List[tuple]:
    """
    Parse the worksheet into individual problems.
    
    Each problem consists of:
    - Multiple lines of numbers (one number per line, arranged vertically)
    - One line with the operator (+, *)
    - Problems are separated by columns of spaces
    
    Args:
        lines: List of lines from the worksheet
        
    Returns:
        List of problems, where each problem is (numbers, operator)
    """
    if not lines:
        return []
    
    # Find maximum line length for column-based parsing
    max_len = max(len(line) for line in lines) if lines else 0
    
    # Convert to grid (pad all lines to same length)
    grid = []
    for line in lines:
        padded = line.ljust(max_len)
        grid.append(padded)
    
    num_rows = len(grid)
    problems = []
    
    # Parse column by column
    col = 0
    while col < max_len:
        # Skip separator columns (all spaces)
        if all(grid[row][col] == ' ' for row in range(num_rows)):
            col += 1
            continue
        
        # Found start of a problem - find its end
        start_col = col
        end_col = col
        
        # Find where this problem ends (next all-space column)
        while end_col < max_len:
            if all(grid[row][end_col] == ' ' for row in range(num_rows)):
                break
            end_col += 1
        
        # Extract this problem's column
        problem_numbers = []
        operator = None
        
        for row in range(num_rows):
            # Extract text from this problem's columns
            text = ''.join(grid[row][start_col:end_col]).strip()
            
            if not text:
                continue
            
            if text in ['+', '*']:
                operator = text
            else:
                # Try to parse as integer
                try:
                    num = int(text)
                    problem_numbers.append(num)
                except ValueError:
                    pass
        
        if problem_numbers and operator:
            problems.append((problem_numbers, operator))
        
        col = end_col
    
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
    problems = parse_problems(lines)
    result = calculate_grand_total(problems)
    print(result)


if __name__ == "__main__":
    main()

