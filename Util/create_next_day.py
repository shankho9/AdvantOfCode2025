#!/usr/bin/env python3
"""
Utility script to automatically create the next day's folder structure for AOC 2025.
Creates a new day folder with Prob1 and Prob2 subfolders, each containing
a blank Python file and input.txt file.
"""

import os
import re
from pathlib import Path


def find_last_day_folder(root_dir: str) -> int:
    """
    Find the highest numbered day folder in the root directory.
    
    Args:
        root_dir: Root directory path
        
    Returns:
        The day number of the last folder, or 0 if none found
    """
    max_day = 0
    pattern = re.compile(r'^(\d+)Dec', re.IGNORECASE)
    
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            match = pattern.match(item)
            if match:
                day_num = int(match.group(1))
                max_day = max(max_day, day_num)
    
    return max_day


def create_day_structure(root_dir: str, day_num: int) -> None:
    """
    Create the folder structure for a given day.
    
    Args:
        root_dir: Root directory path
        day_num: Day number (e.g., 5 for 5Dec)
    """
    # Create main day folder (e.g., "5Dec")
    day_folder_name = f"{day_num}Dec"
    day_folder_path = os.path.join(root_dir, day_folder_name)
    os.makedirs(day_folder_path, exist_ok=True)
    print(f"Created folder: {day_folder_name}")
    
    # Create Prob1 and Prob2 folders
    for prob_num in [1, 2]:
        prob_folder_name = f"Prob{prob_num}"
        prob_folder_path = os.path.join(day_folder_path, prob_folder_name)
        os.makedirs(prob_folder_path, exist_ok=True)
        print(f"  Created subfolder: {prob_folder_name}")
        
        # Create Python file
        py_file_name = f"prob_day{day_num}.py"
        py_file_path = os.path.join(prob_folder_path, py_file_name)
        with open(py_file_path, 'w') as f:
            pass  # Create empty file
        print(f"    Created: {py_file_name}")
        
        # Create input.txt file
        input_file_path = os.path.join(prob_folder_path, "input.txt")
        with open(input_file_path, 'w') as f:
            pass  # Create empty file
        print(f"    Created: input.txt")


def main():
    """Main function to create the next day's folder structure."""
    # Get the root directory (parent of Util folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Find the last day folder
    last_day = find_last_day_folder(root_dir)
    next_day = last_day + 1
    
    print(f"Last day found: {last_day}Dec")
    print(f"Creating structure for: {next_day}Dec")
    print()
    
    # Create the new day structure
    create_day_structure(root_dir, next_day)
    
    print()
    print(f"Successfully created folder structure for Day {next_day}!")


if __name__ == "__main__":
    main()

