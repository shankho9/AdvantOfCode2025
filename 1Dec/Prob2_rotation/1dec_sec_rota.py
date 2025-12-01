def read_rotations(filename):
    """Read rotations from a file, one per line."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def count_zeros_during_rotation(start_position, rotation, max_number=99):
    """
    Count how many times the dial points at 0 DURING a rotation,
    including all intermediate positions visited during the rotation.
    
    Important: We count zeros we arrive at during the rotation, not the starting position.
    A rotation involves 'distance' clicks (movements), so we check positions 1 through distance.
    
    Args:
        start_position: Starting position of the dial (0-99)
        rotation: String like 'L68' or 'R48'
        max_number: Maximum number on the dial (default 99)
    
    Returns:
        Tuple of (count of zeros during rotation, final position after rotation)
    """
    direction = rotation[0]  # L or R
    distance = int(rotation[1:])  # Extract the number
    modulo = max_number + 1  # 100
    
    zero_count = 0
    
    if direction == 'R':
        # Rotate right (increment)
        # Each click moves us one position to the right
        # We check positions we arrive at: start+1, start+2, ..., start+distance (all mod 100)
        for i in range(1, distance + 1):
            current_pos = (start_position + i) % modulo
            if current_pos == 0:
                zero_count += 1
        final_position = (start_position + distance) % modulo
    elif direction == 'L':
        # Rotate left (decrement)
        # Each click moves us one position to the left
        # We check positions we arrive at: start-1, start-2, ..., start-distance (all mod 100)
        for i in range(1, distance + 1):
            current_pos = (start_position - i) % modulo
            if current_pos == 0:
                zero_count += 1
        final_position = (start_position - distance) % modulo
    else:
        raise ValueError(f"Invalid direction: {direction}. Must be L or R.")
    
    return zero_count, final_position


def count_zero_positions_during_rotations(filename):
    """
    Count how many times the dial points at 0 during rotations,
    including all intermediate positions, not just at the end.
    
    Args:
        filename: Path to the input file with rotations
    
    Returns:
        Count of times dial points at 0 during any rotation
    """
    rotations = read_rotations(filename)
    position = 50  # Starting position
    zero_count = 0
    
    # Process each rotation and count zeros during the rotation
    for rotation in rotations:
        zeros_in_rotation, position = count_zeros_during_rotation(position, rotation)
        zero_count += zeros_in_rotation
    
    return zero_count


def main():
    # You can change this to your input file path
    input_file = "input.txt"
    
    try:
        count = count_zero_positions_during_rotations(input_file)
        print(f"The password is: {count}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        print("Please create an input.txt file with the rotations.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

