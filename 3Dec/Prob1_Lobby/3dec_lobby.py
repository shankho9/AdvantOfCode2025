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


def max_joltage_from_bank(bank: str) -> int:
    """
    Find the maximum two-digit joltage possible from a bank.
    Must select exactly two batteries (digits) in order.
    
    Args:
        bank: String of digits representing battery joltages
        
    Returns:
        Maximum two-digit number that can be formed
    """
    if len(bank) < 2:
        return 0
    
    max_joltage = 0
    
    # Try all pairs of positions (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form two-digit number: first digit at i, second digit at j
            joltage = int(bank[i]) * 10 + int(bank[j])
            max_joltage = max(max_joltage, joltage)
    
    return max_joltage


def total_output_joltage(banks: List[str]) -> int:
    """
    Calculate the total output joltage by summing the maximum joltage
    from each bank.
    """
    total = 0
    for bank in banks:
        max_jolt = max_joltage_from_bank(bank)
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








