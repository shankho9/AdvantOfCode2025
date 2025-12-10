from __future__ import annotations

import os
from typing import List


def read_grid_from_file(path: str) -> List[str]:
    """
    Read input file where each line represents a row of the grid.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def count_adjacent_rolls(grid: List[List[str]], row: int, col: int) -> int:
    """
    Count the number of rolls of paper (@) in the 8 adjacent positions
    (including diagonals) around the given position.
    
    Args:
        grid: The grid as a list of lists of characters
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


def remove_accessible_rolls_iteratively(grid: List[str]) -> int:
    """
    Iteratively remove rolls of paper that can be accessed (have < 4 adjacent rolls).
    After each removal, check if more rolls become accessible.
    Continue until no more rolls can be removed.
    
    Args:
        grid: The grid as a list of strings
        
    Returns:
        Total number of rolls removed
    """
    if not grid:
        return 0
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Convert to list of lists for mutability
    mutable_grid = [list(row) for row in grid]
    
    total_removed = 0
    
    # Keep removing rolls until no more can be removed
    while True:
        # Find all rolls that can be accessed in this iteration
        to_remove = []
        
        for row in range(rows):
            for col in range(cols):
                # Only check positions that still have a roll of paper
                if mutable_grid[row][col] == '@':
                    adjacent_count = count_adjacent_rolls(mutable_grid, row, col)
                    # Accessible if fewer than 4 adjacent rolls
                    if adjacent_count < 4:
                        to_remove.append((row, col))
        
        # If no rolls can be removed, we're done
        if not to_remove:
            break
        
        # Remove all accessible rolls
        for row, col in to_remove:
            mutable_grid[row][col] = '.'
            total_removed += 1
    
    return total_removed


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    grid = read_grid_from_file(input_path)
    result = remove_accessible_rolls_iteratively(grid)
    print(result)


if __name__ == "__main__":
    main()






