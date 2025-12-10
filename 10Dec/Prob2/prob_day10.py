# solve_part2_ilp.py

import re
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, PULP_CBC_CMD

def solve_machine(target, buttons):
    """
    target : list[int] (counter targets)
    buttons : list[list[int]] (each button increments listed counters)
    returns min presses for this machine (int), or None if no solution.
    """
    m = len(target)
    n = len(buttons)

    prob = LpProblem("machine", LpMinimize)

    # Variables: x_j = number of times to press button j
    x = [LpVariable(f"x_{j}", lowBound=0, cat=LpInteger) for j in range(n)]

    # Constraints: for each counter i, sum_j (A[i][j] * x_j) == target[i]
    for i in range(m):
        prob += lpSum((1 if i in buttons[j] else 0) * x[j] for j in range(n)) == target[i]

    # Objective: minimize total presses
    prob += lpSum(x[j] for j in range(n))

    # Solve
    status = prob.solve(PULP_CBC_CMD(msg=False))
    if status != 1:  # 1 = "optimal"
        return None
    return sum(int(var.value()) for var in x)

def main():
    total = 0
    with open("input.txt") as f:
        lines = [l.strip() for l in f if l.strip()]

    for line in lines:
        # parse target jolts
        m = re.search(r"\{([^}]*)\}", line)
        assert m, f"No {{}} block in line: {line}"
        req_str = m.group(1).strip()
        target = [int(s) for s in req_str.split(",")] if req_str else []

        # parse buttons
        btn_texts = re.findall(r"\(([^)]*)\)", line)
        buttons = []
        for bt in btn_texts:
            if bt.strip() == "":
                buttons.append([])
            else:
                buttons.append([int(s) for s in bt.split(",")])

        presses = solve_machine(target, buttons)
        if presses is None:
            print("No solution for machine:", line)
            return
        total += presses

    print("Total presses:", total)

if __name__ == "__main__":
    main()
