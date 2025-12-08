#!/usr/bin/env python3
"""
connect_junctions.py

Reads 3D points from input.txt (one 'X,Y,Z' per line).
Finds the 1000 pairs of points with smallest Euclidean distance (ties arbitrary),
connects those pairs (union), and prints the product of the sizes of the
three largest connected components.

If there are fewer than 1000 pairs available, uses all pairs.
"""

import heapq
import math
import sys
from typing import List, Tuple

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

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
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def component_sizes(self) -> List[int]:
        roots = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            roots[r] = roots.get(r, 0) + 1
        return list(roots.values())


def parse_input(path: str = "input.txt") -> List[Tuple[int,int,int]]:
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Bad line in input: {line!r}")
            x, y, z = map(int, (p.strip() for p in parts))
            pts.append((x, y, z))
    return pts


def squared_distance(a: Tuple[int,int,int], b: Tuple[int,int,int]) -> int:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx*dx + dy*dy + dz*dz


def main():
    pts = parse_input("input.txt")
    n = len(pts)
    if n == 0:
        print("0")
        return

    # number of candidate pairs to connect
    total_pairs = n * (n - 1) // 2
    K = min(1000, total_pairs)

    # Use heapq.nsmallest to keep only K smallest distances while iterating pairs.
    # Each item is (squared_distance, i, j)
    def pair_iterator():
        for i in range(n):
            pi = pts[i]
            for j in range(i+1, n):
                yield (squared_distance(pi, pts[j]), i, j)

    smallest = heapq.nsmallest(K, pair_iterator(), key=lambda t: t[0])
    # Sort them ascending by distance to simulate connecting the K shortest pairs in order
    smallest.sort(key=lambda t: t[0])

    dsu = DSU(n)
    for dist2, i, j in smallest:
        dsu.union(i, j)

    sizes = dsu.component_sizes()
    sizes.sort(reverse=True)

    # take top 3 sizes, pad with 1's if fewer than 3 components
    while len(sizes) < 3:
        sizes.append(1)

    a, b, c = sizes[0], sizes[1], sizes[2]
    product = a * b * c

    # Output product (plain) and a short explanation line
    print(product)
    print(f"# Debug: top3 sizes = {a}, {b}, {c}  (connected using {K} shortest pairs)")

if __name__ == "__main__":
    main()
