def read_rotations(filename):
    """Read rotations from a file, one per line."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def apply_rotation(current_position, rotation, max_number=99):
    """
    Apply a rotation to the dial position.
    
    Args:
        current_position: Current position of the dial (0-99)
        rotation: String like 'L68' or 'R48'
        max_number: Maximum number on the dial (default 99)
    
    Returns:
        New position after rotation
    """
    direction = rotation[0]  # L or R
    distance = int(rotation[1:])  # Extract the number
    
    if direction == 'L':
        # Rotate left (subtract, wrap around)
        new_position = (current_position - distance) % (max_number + 1)
    elif direction == 'R':
        # Rotate right (add, wrap around)
        new_position = (current_position + distance) % (max_number + 1)
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be L or R.")
    
    return new_position


def count_zero_positions(filename):
    """
    Count how many times the dial points at 0 after any rotation.
    
    Args:
        filename: Path to the input file with rotations
    
    Returns:
        Count of times dial points at 0
    """
    rotations = read_rotations(filename)
    position = 50  # Starting position
    zero_count = 0
    
    # Check starting position
    if position == 0:
        zero_count += 1
    
    # Process each rotation
    for rotation in rotations:
        position = apply_rotation(position, rotation)
        if position == 0:
            zero_count += 1
    
    return zero_count


def main():
    # You can change this to your input file path
    input_file = "input.txt"
    
    try:
        count = count_zero_positions(input_file)
        print(f"The password is: {count}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        print("Please create an input.txt file with the rotations.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

