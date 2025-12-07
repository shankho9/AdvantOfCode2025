from collections import deque

def solve_tachyon_manifold(grid):
    """
    Simulate tachyon beam splitting in the manifold.
    Beams always move downward (row increases).
    Count every time a beam hits a '^' splitter.
    """
    if not grid:
        return 0
    
    rows = len(grid)
    cols = len(grid[0])
    
    # Find starting position 'S'
    start_col = -1
    for col in range(cols):
        for row in range(rows):
            if grid[row][col] == 'S':
                start_col = col
                break
        if start_col != -1:
            break
    
    if start_col == -1:
        print("No 'S' found!")
        return 0
    
    # Each beam is (row, col)
    beams = deque([(0, start_col)])
    splits = 0
    
    visited = set()  # Track positions to avoid infinite loops
    
    while beams:
        row, col = beams.popleft()
        
        # Out of bounds = exited manifold
        if row >= rows or col < 0 or col >= cols:
            continue
            
        pos = (row, col)
        if pos in visited:
            continue
        visited.add(pos)
        
        cell = grid[row][col]
        
        if cell == '^':
            splits += 1
            # Split: emit new beams left and right at NEXT row
            if row + 1 < rows:
                if col - 1 >= 0:
                    beams.append((row + 1, col - 1))
                if col + 1 < cols:
                    beams.append((row + 1, col + 1))
        else:
            # Continue downward
            beams.append((row + 1, col))
    
    return splits

# Read input from input.txt
try:
    with open('input.txt', 'r') as f:
        grid = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Error: input.txt not found in current directory!")
    exit(1)

# Solve
result = solve_tachyon_manifold(grid)
print(f"Beam splits: {result}")
