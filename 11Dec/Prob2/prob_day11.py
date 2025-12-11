def solve_part2():
    # Read and parse input
    graph = {}
    with open("input.txt") as f:
        for line in f.read().strip().splitlines():
            if not line.strip():
                continue
            name, rhs = line.split(":")
            parent = name.strip()
            children = rhs.strip().split()
            graph[parent] = children

    START = "svr"
    END = "out"
    MUST_HAVE = {"dac", "fft"}

    # Memoization for: (node, visited_dac, visited_fft)
    memo = {}

    def dfs(node, has_dac, has_fft):
        # If reach out, count only if both flags true
        if node == END:
            return 1 if (has_dac and has_fft) else 0

        key = (node, has_dac, has_fft)
        if key in memo:
            return memo[key]

        total = 0
        for nxt in graph.get(node, []):
            nd = has_dac or (nxt == "dac")
            nf = has_fft or (nxt == "fft")
            total += dfs(nxt, nd, nf)

        memo[key] = total
        return total

    # Starting state (svr is not dac/fft)
    print(dfs(START, False, False))


if __name__ == "__main__":
    solve_part2()
