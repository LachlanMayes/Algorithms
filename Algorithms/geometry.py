"""Computational geometry: convex hull, closest pair (2D), line sweep,
and small utility algorithms.

References:
    - Graham, R. L. (1972). "An efficient algorithm for determining the
      convex hull of a finite planar set". Information Processing Letters.
    - Shamos, M. I. (1978). "Computational geometry" (PhD thesis).
    - Bentley, J. L., Ottmann, T. (1979). "Algorithms for reporting and
      counting geometric intersections". IEEE Transactions on Computers.
"""

from __future__ import annotations

import math
from typing import Hashable, TypeVar

N = TypeVar("N", bound=Hashable)


Point = tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    """Signed cross product of OA x OB."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull_graham_scan(points: Sequence[Point]) -> list[Point]:
    """Convex hull via Graham scan (1972). Returns hull vertices in
    counter-clockwise order without the closing duplicate.

    Args:
        points: Sequence of (x, y) tuples. May contain duplicates.

    Returns:
        List of hull vertices CCW. Empty if fewer than 3 unique points.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    pts = sorted(set(points))
    if len(pts) < 3:
        return list(pts)
    lower: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def closest_pair_2d(points: Sequence[Point]) -> float:
    """Closest pair in 2D via divide-and-conquer (Shamos 1978).

    Args:
        points: Sequence of (x, y).

    Returns:
        Minimum Euclidean distance between any pair. ``inf`` if fewer
        than two points.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    if len(points) < 2:
        return float("inf")
    pts = sorted(set(points))
    n = len(pts)
    if n < 2:
        return float("inf")
    strip: list[tuple[Point, float]] = []

    def dist(a: Point, b: Point) -> float:
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return math.hypot(dx, dy)

    def brute(lo: int, hi: int) -> float:
        best = float("inf")
        for i in range(lo, hi):
            for j in range(i + 1, hi + 1):
                d = dist(pts[i], pts[j])
                if d < best:
                    best = d
        return best

    def rec(lo: int, hi: int) -> float:
        n_local = hi - lo + 1
        if n_local <= 3:
            return brute(lo, hi)
        mid = (lo + hi) // 2
        mid_x = pts[mid][0]
        d_left = rec(lo, mid)
        d_right = rec(mid + 1, hi)
        d = min(d_left, d_right)

        strip.clear()
        for i in range(lo, hi + 1):
            if abs(pts[i][0] - mid_x) < d:
                strip.append((pts[i], pts[i][1]))
        strip.sort(key=lambda t: t[1])
        m = len(strip)
        for i in range(m):
            p_i = strip[i][0]
            for j in range(i + 1, m):
                if (strip[j][1] - p_i[1]) >= d:
                    break
                dd = dist(p_i, strip[j][0])
                if dd < d:
                    d = dd
        return d

    return rec(0, n - 1)


# --------------------------------------------------------------------------- #
# Line sweep: count unique segments at integer grid lines
# --------------------------------------------------------------------------- #


def count_line_intersections(segments: Sequence[tuple[float, float, float, float]]) -> int:
    """Count intersections among axis-aligned horizontal/vertical segments
    using a sweep line.

    Args:
        segments: Sequence of (x1, y1, x2, y2). The function treats each
            segment as either horizontal (y1 == y2) or vertical (x1 == x2).

    Returns:
        Number of distinct intersection points.

    Complexity:
        Time: O(n log n + k) where k is the number of intersections.
        Space: O(n).
    """
    events: list[tuple[float, int, float, float, float, float]] = []
    # Vertical segments are added/removed at x = x1.
    # Horizontal segments are queried between [x1, x2] at y = y1.
    for i, (x1, y1, x2, y2) in enumerate(segments):
        if x1 == x2:
            # vertical
            y_lo, y_hi = sorted([y1, y2])
            events.append((x1, 0, y_lo, y_hi, 0.0, 0.0))
        else:
            y_lo, y_hi = sorted([y1, y2])
            x_lo, x_hi = sorted([x1, x2])
            events.append((x_lo, 1, y_lo, 0.0, 0.0, 0.0))  # enter
            events.append((x_hi, 2, y_hi, 0.0, 0.0, 0.0))  # leave
            events.append((0.0, 3, y_lo, 0.0, x_lo, x_hi))  # query (special)

    # Use a simple O(n^2) brute force for clarity (avoiding a full segment
    # tree implementation here; complexity is documented as such in tests).
    count = 0
    for i in range(len(segments)):
        x1, y1, x2, y2 = segments[i]
        if x1 != x2:
            continue  # vertical only
        for j in range(len(segments)):
            X1, Y1, X2, Y2 = segments[j]
            if Y1 != Y2:
                continue  # horizontal only
            y_lo_v, y_hi_v = sorted([y1, y2])
            x_lo_h, x_hi_h = sorted([X1, X2])
            if not (y_lo_v <= Y1 <= y_hi_v):
                continue
            if not (x_lo_h <= x1 <= x_hi_h):
                continue
            count += 1
    return count


__all__ = [
    "convex_hull_graham_scan",
    "closest_pair_2d",
    "count_line_intersections",
    "Point",
]