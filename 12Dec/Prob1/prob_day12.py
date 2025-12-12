#!/usr/bin/env python3

import re

# ---------------------------------------------------------
# Parse input
# ---------------------------------------------------------
def parse_input(fname="input.txt"):
    with open(fname) as f:
        lines = [l.rstrip() for l in f]

    shapes = []
    regions = []

    i = 0
    shape_re = re.compile(r"^(\d+):$")
    region_re = re.compile(r"^(\d+)x(\d+):\s+(.*)$")

    # Parse shapes
    while i < len(lines):
        m = shape_re.match(lines[i])
        if not m:
            i += 1
            continue
        i += 1
        block = []
        while i < len(lines) and re.search(r"[.#]", lines[i]):
            block.append(lines[i])
            i += 1
        shapes.append(block)

    # Parse regions
    for ln in lines:
        m = region_re.match(ln)
        if m:
            w = int(m.group(1))
            h = int(m.group(2))
            counts = list(map(int, m.group(3).split()))
            regions.append((w, h, counts))

    return shapes, regions

# ---------------------------------------------------------
# Shape utilities
# ---------------------------------------------------------
def norm(cells):
    minx = min(x for x, y in cells)
    miny = min(y for x, y in cells)
    return frozenset((x - minx, y - miny) for x, y in cells)

def rotations_and_flips(cells):
    """Generate all 8 transforms."""
    out = set()
    for fx in (1, -1):
        for fy in (1, -1):
            for r in range(4):  # rotate 4 times
                pts = []
                for x, y in cells:
                    x, y = fx*x, fy*y
                    for _ in range(r):
                        x, y = -y, x
                    pts.append((x, y))
                out.add(norm(pts))
    return out

def shape_cells(shape_rows):
    pts = [(x, y)
           for y, row in enumerate(shape_rows)
           for x, c in enumerate(row) if c == '#']
    return norm(pts)

# ---------------------------------------------------------
# Fit solver (backtracking)
# ---------------------------------------------------------
def placements_for_shape(shape, w, h):
    """Return list of placements: each is set of cell indices."""
    out = []
    maxx = max(x for x, y in shape)
    maxy = max(y for x, y in shape)
    for ox in range(w - maxx):
        for oy in range(h - maxy):
            cells = []
            ok = True
            for x, y in shape:
                gx = ox + x
                gy = oy + y
                if gx < 0 or gx >= w or gy < 0 or gy >= h:
                    ok = False
                    break
                cells.append(gy * w + gx)
            if ok:
                out.append(frozenset(cells))
    return out

def can_fit(w, h, shapes, counts):
    total_area_needed = sum(len(shapes[i]) * counts[i] for i in range(len(counts)))
    if total_area_needed > w * h:
        return False

    # Precompute all possible placements for each shape index
    all_placements = []
    for i in range(len(shapes)):
        if counts[i] == 0:
            all_placements.append([])
            continue
        plist = []
        for t in rotations_and_flips(shapes[i]):
            plist.extend(placements_for_shape(t, w, h))
        all_placements.append(plist)
        if counts[i] > 0 and len(plist) == 0:
            return False

    grid_used = set()

    # Sort shapes by descending area for better pruning
    order = sorted(range(len(counts)),
                   key=lambda i: -len(shapes[i]))

    def backtrack(idx):
        if idx == len(order):
            return True

        si = order[idx]
        need = counts[si]
        if need == 0:
            return backtrack(idx + 1)

        # choose placements
        for placement in all_placements[si]:
            if placement & grid_used:
                continue
            # place
            grid_used.update(placement)
            counts[si] -= 1
            if counts[si] == 0:
                ok = backtrack(idx + 1)
            else:
                ok = backtrack(idx)     # need more copies of same shape
            # undo
            counts[si] += 1
            grid_used.difference_update(placement)
            if ok:
                return True
        return False

    return backtrack(0)

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    shapes_raw, regions = parse_input()
    # convert shapes to cell sets
    shapes = [shape_cells(sh) for sh in shapes_raw]

    fit = 0
    for (w, h, counts) in regions:
        # pad counts
        if len(counts) < len(shapes):
            counts = counts + [0]*(len(shapes)-len(counts))

        if can_fit(w, h, shapes, counts[:]):   # pass copy
            fit += 1

    print(fit)

if __name__ == "__main__":
    main()
