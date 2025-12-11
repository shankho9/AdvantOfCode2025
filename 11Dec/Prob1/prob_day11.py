def solve():
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

    start = "you"
    end = "out"

    # Memoization to avoid recomputing
    memo = {}

    def dfs(node):
        # If we reach 'out', this is 1 valid path
        if node == end:
            return 1

        # If already computed, reuse
        if node in memo:
            return memo[node]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)

        memo[node] = total
        return total

    print(dfs(start))


if __name__ == "__main__":
    solve()
