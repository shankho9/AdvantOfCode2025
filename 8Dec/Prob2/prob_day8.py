#!/usr/bin/env python3
"""
Part 2:
Continue connecting the closest unconnected pairs until
ALL junction boxes are in a single circuit.

Output: product of X-coordinates of the LAST connected pair.
"""

import heapq
from typing import List, Tuple

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


def parse_input(path="input.txt"):
    pts = []
    with open(path, "r") as f:
        for line in f:
            if "," in line:
                x, y, z = map(int, line.strip().split(","))
                pts.append((x, y, z))
    return pts


def squared_distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx*dx + dy*dy + dz*dz


def main():
    pts = parse_input("input.txt")
    n = len(pts)
    dsu = DSU(n)

    # Build a min-heap of ALL pairs (distance^2, i, j)
    heap = []
    for i in range(n):
        for j in range(i+1, n):
            dist2 = squared_distance(pts[i], pts[j])
            heap.append((dist2, i, j))

    heapq.heapify(heap)

    last_pair = None

    # Keep popping the closest unused pair until all components = 1
    while dsu.components > 1:
        dist2, i, j = heapq.heappop(heap)
        if dsu.union(i, j):      # this pair actually connected two different circuits
            last_pair = (i, j)

    # Extract X coordinates of the last connected pair
    i, j = last_pair
    x1 = pts[i][0]
    x2 = pts[j][0]
    product = x1 * x2

    print(product)
    print(f"# Debug: last connection was between X={x1} and X={x2}")


if __name__ == "__main__":
    main()
