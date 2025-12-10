# largest_rectangle_inclusive.py
import re

def read_input(fn="input.txt"):
    pts = []
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            # permissive parsing: find first two integers on the line
            nums = re.findall(r"-?\d+", s)
            if len(nums) >= 2:
                x, y = int(nums[0]), int(nums[1])
                pts.append((x, y))
    return pts

def largest_inclusive_area(points):
    n = len(points)
    if n < 2:
        return 0, None
    max_area = 0
    best_pair = None
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i+1, n):
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1   # inclusive
            height = abs(y1 - y2) + 1  # inclusive
            area = width * height
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2), width, height)
    return max_area, best_pair

if __name__ == "__main__":
    pts = read_input("input.txt")
    pts = list(dict.fromkeys(pts))  # preserve order and remove duplicates
    area, info = largest_inclusive_area(pts)
    if info:
        (x1,y1),(x2,y2),w,h = info
        print(f"Points read: {len(pts)}")
        print(f"Largest inclusive rectangle area: {area}")
        print(f"Between corners: ({x1},{y1}) and ({x2},{y2})")
        print(f"Width = {w}, Height = {h} (inclusive)")
    else:
        print("Not enough points to form a rectangle.")
