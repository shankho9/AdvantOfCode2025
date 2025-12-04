from __future__ import annotations

import os
from typing import List


def read_banks_from_file(path: str) -> List[str]:
    """
    Read input file where each line is a bank of batteries (a string of digits).
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def max_joltage_from_bank(bank: str, k: int = 12) -> int:
    """
    Find the maximum k-digit joltage possible from a bank.
    Must select exactly k batteries (digits) in order.
    
    Uses a greedy algorithm: for each position in the result, pick the largest
    digit possible while ensuring we can still pick enough remaining digits.
    
    Args:
        bank: String of digits representing battery joltages
        k: Number of digits to select (default 12)
        
    Returns:
        Maximum k-digit number that can be formed
    """
    n = len(bank)
    if n < k:
        return 0
    
    if n == k:
        return int(bank)
    
    result_digits = []
    start_idx = 0
    
    # For each position in the result (0 to k-1)
    for pos in range(k):
        # We need to pick (k - pos) more digits
        # We can look at digits from start_idx to (n - (k - pos) + 1)
        # to ensure we have enough digits left
        end_idx = n - (k - pos) + 1
        
        # Find the maximum digit in the allowed range
        max_digit = -1
        max_idx = -1
        for i in range(start_idx, end_idx):
            digit = int(bank[i])
            if digit > max_digit:
                max_digit = digit
                max_idx = i
        
        # Add the maximum digit to result
        result_digits.append(str(max_digit))
        # Start next search from after the selected position
        start_idx = max_idx + 1
    
    return int(''.join(result_digits))


def total_output_joltage(banks: List[str]) -> int:
    """
    Calculate the total output joltage by summing the maximum joltage
    from each bank (selecting exactly 12 digits from each).
    """
    total = 0
    for bank in banks:
        max_jolt = max_joltage_from_bank(bank, k=12)
        total += max_jolt
    return total


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(here, "input.txt")
    
    banks = read_banks_from_file(input_path)
    result = total_output_joltage(banks)
    print(result)


if __name__ == "__main__":
    main()


