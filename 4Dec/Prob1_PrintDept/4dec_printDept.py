from __future__ import annotations

import os
from typing import List, Tuple


def read_grid_from_file(path: str) -> List[str]:
    """
    Read input file where each line represents a row of the grid.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def count_adjacent_rolls(grid: List[str], row: int, col: int) -> int:
    """
    Count the number of rolls of paper (@) in the 8 adjacent positions
    (including diagonals) around the given position.
    
    Args:
        grid: The grid as a list of strings
        row: Row index
        col: Column index
        
    Returns:
        Number of adjacent rolls (0-8)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    count = 0
    # Check all 8 neighbors: up, down, left, right, and 4 diagonals
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the position itself
            
            new_row = row + dr
            new_col = col + dc
            
            # Check if position is within bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] == '@':
                    count += 1
    
    return count


def count_accessible_rolls(grid: List[str]) -> int:
    """
    Count how many rolls of paper can be accessed by a forklift.
    A roll can be accessed if it has fewer than 4 adjacent rolls.
    
    Args:
        grid: The grid as a list of strings
        
    Returns:
        Number of accessible rolls
    """
    if not grid:
        return 0
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(rows):
        for col in range(cols):
            # Only check positions that have a roll of paper
            if grid[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid, row, col)
                # Accessible if fewer than 4 adjacent rolls
                if adjacent_count < 4:
                    accessible_count += 1
    
    return accessible_count


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    grid = read_grid_from_file(input_path)
    result = count_accessible_rolls(grid)
    print(result)


if __name__ == "__main__":
    main()

