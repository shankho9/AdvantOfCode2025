from __future__ import annotations

import os
from typing import List, Tuple


def read_input_file(path: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Read input file with fresh ingredient ID ranges and available ingredient IDs.
    
    Format:
    - First section: ranges (one per line, format "start-end")
    - Blank line
    - Second section: available IDs (one per line)
    
    Args:
        path: Path to input file
        
    Returns:
        Tuple of (ranges, available_ids)
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by blank line
    parts = content.split("\n\n")
    
    if len(parts) < 2:
        # Try splitting by double newline or handle single section
        parts = content.strip().split("\n\n")
        if len(parts) < 2:
            # Look for first empty line
            lines = content.split("\n")
            blank_line_idx = -1
            for i, line in enumerate(lines):
                if not line.strip():
                    blank_line_idx = i
                    break
            
            if blank_line_idx >= 0:
                range_lines = lines[:blank_line_idx]
                id_lines = lines[blank_line_idx + 1:]
            else:
                range_lines = []
                id_lines = lines
        else:
            range_lines = parts[0].strip().split("\n")
            id_lines = parts[1].strip().split("\n")
    else:
        range_lines = parts[0].strip().split("\n")
        id_lines = parts[1].strip().split("\n")
    
    # Parse ranges
    ranges = []
    for line in range_lines:
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        ranges.append((int(start_str), int(end_str)))
    
    # Parse available IDs
    available_ids = []
    for line in id_lines:
        line = line.strip()
        if not line:
            continue
        available_ids.append(int(line))
    
    return ranges, available_ids


def is_fresh(ingredient_id: int, ranges: List[Tuple[int, int]]) -> bool:
    """
    Check if an ingredient ID is fresh (falls into any range).
    
    Args:
        ingredient_id: The ingredient ID to check
        ranges: List of (start, end) inclusive ranges
        
    Returns:
        True if the ID is in any range, False otherwise
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(ranges: List[Tuple[int, int]], available_ids: List[int]) -> int:
    """
    Count how many available ingredient IDs are fresh.
    
    Args:
        ranges: List of fresh ingredient ID ranges
        available_ids: List of available ingredient IDs to check
        
    Returns:
        Number of fresh ingredient IDs
    """
    count = 0
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, ranges):
            count += 1
    return count


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    ranges, available_ids = read_input_file(input_path)
    result = count_fresh_ingredients(ranges, available_ids)
    print(result)


if __name__ == "__main__":
    main()






