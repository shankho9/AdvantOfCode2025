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


def is_in_any_range(n: int, starts, ends) -> bool:
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
    Now, an ID is invalid if it is made only of some sequence of digits
    repeated at least twice (no leading zeroes).

    This function sums all such invalid IDs that lie within any of the given ranges.
    """
    if not ranges:
        return 0

    merged = merge_ranges(ranges)
    starts, ends = build_range_index(merged)

    global_min = min(s for s, _ in merged)
    global_max = max(e for _, e in merged)

    max_digits = len(str(global_max))
    invalid_ids = set()

    # Generate all numbers within [global_min, global_max] that consist of
    # some digit block repeated k times (k >= 2).
    #
    # Let block length be L, repeated k times:
    #   total digits D = L * k
    # We require D <= max_digits.
    #
    # For each L and k, we iterate base blocks from 10^(L-1) to 10^L - 1
    # (no leading zero) and build the repeated number.
    for L in range(1, max_digits + 1):
        # k must be at least 2 and such that total digits <= max_digits
        max_k = max_digits // L
        if max_k < 2:
            continue

        for k in range(2, max_k + 1):
            # For this (L, k), total digits is L * k.
            block_start = 10 ** (L - 1)  # first digit can't be 0
            block_end = 10**L - 1

            for block in range(block_start, block_end + 1):
                s = str(block) * k
                n = int(s)

                if n < global_min:
                    continue
                if n > global_max:
                    # For increasing block, n will only grow; break for this k.
                    break

                if is_in_any_range(n, starts, ends):
                    invalid_ids.add(n)

    return sum(invalid_ids)


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")

    ranges = read_ranges_from_file(input_path)
    result = sum_invalid_ids(ranges)
    print(result)


if __name__ == "__main__":
    main()


