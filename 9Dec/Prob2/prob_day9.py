# largest_redgreen_rectangle.py
# Finds the largest axis-aligned rectangle (inclusive tiles) whose opposite corners
# are red tiles from input.txt, and whose entire area is inside the polygon formed
# by the red points (boundary + interior = allowed tiles).

import math, bisect, time, sys
from collections import defaultdict

def read_points(fn="input.txt"):
    pts = []
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            x,y = map(int, s.split(","))
            pts.append((x,y))
    return pts

def build_edges(pts):
    if pts[0] != pts[-1]:
        pts = pts[:] + [pts[0]]
    edges = []
    for i in range(len(pts)-1):
        x1,y1 = pts[i]
        x2,y2 = pts[i+1]
        edges.append((x1,y1,x2,y2))
    return edges, pts

def compute_row_intervals(edges, min_y, max_y):
    """Compute, for each integer tile row y in [min_y,max_y], the merged inclusive
    integer x-intervals (x_start..x_end) whose tile centers (x+0.5, y+0.5)
    fall inside the polygon (even-odd scanline).
    Returns dict: y -> tuple((x0,x1),(x2,x3),...)
    """
    row_intervals = {}
    for y in range(min_y, max_y+1):
        yc = y + 0.5
        xs = []
        for (x1,y1,x2,y2) in edges:
            if y1 == y2:
                continue
            ymin = min(y1,y2)
            ymax = max(y1,y2)
            # half-open rule: include edges where yc in [ymin, ymax)
            if yc < ymin or yc >= ymax:
                continue
            t = (yc - y1) / (y2 - y1)
            xi = x1 + t * (x2 - x1)
            xs.append(xi)
        if not xs:
            continue
        xs.sort()
        intervals = []
        for i in range(0, len(xs), 2):
            xl = xs[i]
            xr = xs[i+1]
            x_start = math.ceil(xl - 0.5 - 1e-9)
            x_end = math.floor(xr - 0.5 + 1e-9)
            if x_start <= x_end:
                intervals.append((x_start, x_end))
        if intervals:
            # merge contiguous/overlapping integer intervals
            merged = []
            intervals.sort()
            cs, ce = intervals[0]
            for s,e in intervals[1:]:
                if s <= ce + 1:
                    ce = max(ce, e)
                else:
                    merged.append((cs, ce))
                    cs, ce = s, e
            merged.append((cs, ce))
            row_intervals[y] = tuple(merged)
    return row_intervals

def compress_row_blocks(row_intervals):
    """Compress consecutive rows y with identical interval lists into blocks:
       list of (y_start, y_end, intervals)
    """
    items = sorted(row_intervals.items())
    blocks = []
    if not items:
        return blocks
    cur_y, cur_iv = items[0]
    start_y = cur_y
    prev_y = cur_y
    for y, iv in items[1:]:
        if iv == cur_iv and y == prev_y + 1:
            prev_y = y
            continue
        blocks.append((start_y, prev_y, cur_iv))
        start_y = y
        prev_y = y
        cur_iv = iv
    blocks.append((start_y, prev_y, cur_iv))
    return blocks

def solve(points):
    edges, pts_closed = build_edges(points)
    ys = [p[1] for p in pts_closed[:-1]]
    min_y, max_y = min(ys), max(ys)
    # scanline to compute per-row allowed integer x-intervals
    t0 = time.time()
    row_intervals = compute_row_intervals(edges, min_y, max_y)
    t1 = time.time()
    blocks = compress_row_blocks(row_intervals)
    t2 = time.time()

    # prepare red points grouping by y
    unique_reds = list(dict.fromkeys(points))  # preserve order, remove duplicates
    red_xs_by_y = defaultdict(list)
    for x,y in unique_reds:
        red_xs_by_y[y].append(x)
    for y in red_xs_by_y:
        red_xs_by_y[y].sort()
    red_ys = sorted(red_xs_by_y.keys())

    # solve by iterating y1,y2 pairs and intersecting blocks' intervals
    max_area = 0
    best = None
    pairs_checked = 0
    for i, y1 in enumerate(red_ys):
        for y2 in red_ys[i:]:
            pairs_checked += 1
            ymin, ymax = y1, y2
            height = ymax - ymin + 1
            allowed = None
            # intersect allowed intervals with blocks overlapping [ymin,ymax]
            for (bs, be, ivs) in blocks:
                if be < ymin or bs > ymax:
                    continue
                if allowed is None:
                    allowed = list(ivs)
                else:
                    # intersect current allowed with ivs
                    A = allowed
                    B = list(ivs)
                    new_allowed = []
                    a_idx = b_idx = 0
                    while a_idx < len(A) and b_idx < len(B):
                        a1,a2 = A[a_idx]
                        b1,b2 = B[b_idx]
                        s = max(a1,b1)
                        e = min(a2,b2)
                        if s <= e:
                            new_allowed.append((s,e))
                        if a2 < b2:
                            a_idx += 1
                        else:
                            b_idx += 1
                    allowed = new_allowed
                if not allowed:
                    break
            if not allowed:
                continue
            # for each red x at y1 and y2
            for x1 in red_xs_by_y[y1]:
                for x2 in red_xs_by_y[y2]:
                    xmin = min(x1,x2); xmax = max(x1,x2)
                    width = xmax - xmin + 1
                    area = width * height
                    if area <= max_area:
                        continue
                    # check containment: any allowed interval covering [xmin,xmax]?
                    good = any(a <= xmin and b >= xmax for (a,b) in allowed)
                    if good:
                        max_area = area
                        best = ((x1,y1),(x2,y2), width, height)
    t3 = time.time()
    return {
        "max_area": max_area,
        "best": best,
        "timings": (t1-t0, t2-t1, t3-t2),
        "rows_with_coverage": len(row_intervals),
        "blocks": len(blocks),
        "pairs_checked": pairs_checked
    }

if __name__ == "__main__":
    pts = read_points("input.txt")
    result = solve(pts)
    if result["best"]:
        (ax,ay),(bx,by), w,h = result["best"]
        print("Max inclusive area with red+green constraint:", result["max_area"])
        print("Between corners:", (ax,ay), (bx,by))
        print("Width, Height (inclusive):", w, h)
    else:
        print("No valid rectangle found.")
    print("Rows with coverage:", result["rows_with_coverage"], "Blocks:", result["blocks"])
    print("Timings (scanline, compress, checking) seconds:", result["timings"])
