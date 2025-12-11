from __future__ import annotations

import os
from bisect import bisect_right
from typing import List, Tuple


def read_ranges_from_file(path: str) -> List[Tuple[int, int]]:
    """
    Read a single-line input file containing comma-separated ranges like:
    11-22,95-115,998-1012
    and return a list of (start, end) integer tuples.
    """
    with open(path, "r", encoding="utf-8") as f:
        line = f.read().strip()

    if not line:
        return []

    parts = [p.strip() for p in line.split(",") if p.strip()]
    ranges: List[Tuple[int, int]] = []
    for part in parts:
        start_str, end_str = part.split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or touching ranges to make membership checks efficient.
    """
    if not ranges:
        return []

    ranges_sorted = sorted(ranges, key=lambda x: x[0])
    merged: List[Tuple[int, int]] = []
    cur_start, cur_end = ranges_sorted[0]

    for start, end in ranges_sorted[1:]:
        if start <= cur_end + 1:
            # Overlapping or adjacent; extend current range.
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))
    return merged


def build_range_index(ranges: List[Tuple[int, int]]):
    """
    Precompute arrays of starts and ends for binary search.
    """
    starts = [s for s, _ in ranges]
    ends = [e for _, e in ranges]
    return starts, ends


def is_in_any_range(n: int, merged_ranges: List[Tuple[int, int]], starts, ends) -> bool:
    """
    Return True if n is contained in any of the merged (non-overlapping) ranges.
    Uses binary search over range starts.
    """
    idx = bisect_right(starts, n) - 1
    if idx < 0:
        return False
    return n <= ends[idx]


def sum_invalid_ids(ranges: List[Tuple[int, int]]) -> int:
    """
    An ID is invalid if it is made of some sequence of digits repeated twice,
    e.g. 55, 6464, 123123. No leading zeros are allowed.

    This function sums all such invalid IDs that lie within any of the given ranges.
    """
    if not ranges:
        return 0

    merged = merge_ranges(ranges)
    starts, ends = build_range_index(merged)

    global_min = min(s for s, _ in merged)
    global_max = max(e for _, e in merged)

    max_digits = len(str(global_max))
    total = 0

    # Generate all numbers of the form HH within [global_min, global_max].
    for half_len in range(1, max_digits // 2 + 1):
        half_start = 10 ** (half_len - 1)  # no leading zero
        half_end = 10**half_len - 1

        for half in range(half_start, half_end + 1):
            s = str(half)
            n = int(s + s)

            if n < global_min:
                continue
            if n > global_max:
                # For increasing half, n will only grow; we can stop this loop.
                break

            if is_in_any_range(n, merged, starts, ends):
                total += n

    return total


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")

    ranges = read_ranges_from_file(input_path)
    result = sum_invalid_ids(ranges)
    print(result)


if __name__ == "__main__":
    main()












