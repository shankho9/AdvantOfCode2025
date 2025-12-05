from __future__ import annotations

import os
from typing import List, Tuple


def read_ranges_from_file(path: str) -> List[Tuple[int, int]]:
    """
    Read input file and extract only the fresh ingredient ID ranges.
    
    Format:
    - First section: ranges (one per line, format "start-end")
    - Blank line
    - Second section: available IDs (ignored for Part 2)
    
    Args:
        path: Path to input file
        
    Returns:
        List of (start, end) ranges
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by blank line to get first section (ranges)
    parts = content.split("\n\n")
    
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
        else:
            # No blank line, assume all lines are ranges
            range_lines = [line for line in lines if line.strip()]
    else:
        range_lines = parts[0].strip().split("\n")
    
    # Parse ranges
    ranges = []
    for line in range_lines:
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        ranges.append((int(start_str), int(end_str)))
    
    return ranges


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges.
    
    Args:
        ranges: List of (start, end) inclusive ranges
        
    Returns:
        List of merged non-overlapping ranges
    """
    if not ranges:
        return []
    
    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    
    merged = []
    current_start, current_end = sorted_ranges[0]
    
    for start, end in sorted_ranges[1:]:
        # If ranges overlap or are adjacent, merge them
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            # No overlap, add current range and start new one
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    
    # Add the last range
    merged.append((current_start, current_end))
    
    return merged


def count_all_fresh_ids(ranges: List[Tuple[int, int]]) -> int:
    """
    Count all unique ingredient IDs that are considered fresh by any range.
    
    An ingredient ID is fresh if it falls into any range (inclusive).
    Overlapping ranges are merged first, then we count the total IDs.
    
    Args:
        ranges: List of (start, end) inclusive ranges
        
    Returns:
        Total number of unique fresh ingredient IDs
    """
    # Merge overlapping ranges
    merged_ranges = merge_ranges(ranges)
    
    # Count total IDs across all merged ranges
    total = 0
    for start, end in merged_ranges:
        # Range is inclusive, so count is (end - start + 1)
        total += (end - start + 1)
    
    return total


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    ranges = read_ranges_from_file(input_path)
    result = count_all_fresh_ids(ranges)
    print(result)


if __name__ == "__main__":
    main()

