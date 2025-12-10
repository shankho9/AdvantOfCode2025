import re

# ------------------------------------------------------------
# Solve a single machine: find minimum presses to reach target
# ------------------------------------------------------------
def min_button_presses(target_bits, buttons, n):
    """
    target_bits : list[int] (0/1) target light pattern
    buttons     : list[list[int]] button toggle indices
    n           : number of lights
    """

    m = len(buttons)
    # Build matrix A (m x n) and vector b (target)
    A = [[0]*m for _ in range(n)]  # transpose form A^T easier for elimination

    for j, btn in enumerate(buttons):
        for idx in btn:
            A[idx][j] ^= 1

    b = target_bits[:]  # target vector length n

    # Perform Gaussian elimination on A x = b  over GF(2)
    row = 0
    pivot_col = [-1]*n  # pivot column for each row

    for col in range(m):
        # Find pivot row
        pivot = None
        for r in range(row, n):
            if A[r][col] == 1:
                pivot = r
                break

        if pivot is None:
            continue

        # Swap rows
        A[row], A[pivot] = A[pivot], A[row]
        b[row], b[pivot] = b[pivot], b[row]

        pivot_col[row] = col

        # Eliminate downward
        for r in range(n):
            if r != row and A[r][col] == 1:
                for c in range(col, m):
                    A[r][c] ^= A[row][c]
                b[r] ^= b[row]

        row += 1
        if row == n:
            break

    # Check for inconsistent system
    for r in range(n):
        if pivot_col[r] == -1 and b[r] == 1:
            # No solution
            return float('inf')

    # ---------------------------------------------------------
    # Now find minimal Hamming weight solution for free vars.
    # Free variables = variables in columns without pivots.
    # Number of free variables is small (buttons - rank).
    # Try all possibilities (works because constraints small).
    # ---------------------------------------------------------
    pivot_positions = set([p for p in pivot_col if p != -1])
    free_vars = [i for i in range(m) if i not in pivot_positions]

    min_presses = float('inf')

    # brute force small free var count
    from itertools import product

    for setting in product([0,1], repeat=len(free_vars)):
        x = [0]*m
        # set free vars
        for fv, v in zip(free_vars, setting):
            x[fv] = v

        # back substitute to compute pivot vars
        for r in reversed(range(n)):
            pc = pivot_col[r]
            if pc == -1:
                continue
            val = b[r]
            # subtract known free vars
            for c in range(pc+1, m):
                if A[r][c] == 1:
                    val ^= x[c]
            x[pc] = val

        presses = sum(x)
        min_presses = min(min_presses, presses)

    return min_presses


# ------------------------------------------------------------
# Main Parsing + Summation
# ------------------------------------------------------------
def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0

    for line in lines:
        # extract indicator lights
        pattern = re.search(r"\[([.#]+)\]", line).group(1)
        target_bits = [1 if c == "#" else 0 for c in pattern]
        n = len(target_bits)

        # extract buttons (ignore joltage {} block)
        button_texts = re.findall(r"\(([^)]*)\)", line)
        buttons = []
        for bt in button_texts:
            if bt.strip() == "":
                buttons.append([])
            else:
                numbers = [int(x) for x in bt.split(",")]
                buttons.append(numbers)

        # solve machine
        presses = min_button_presses(target_bits, buttons, n)
        total += presses

    print(total)


if __name__ == "__main__":
    main()
