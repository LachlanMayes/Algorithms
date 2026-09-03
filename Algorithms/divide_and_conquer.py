"""Divide-and-conquer algorithms.

These follow the canonical recursion pattern: split the problem into
independent subproblems, solve them recursively, and combine the results.
"""

from __future__ import annotations

import math
from typing import Sequence


def merge_sort(arr: Sequence[int]) -> list[int]:
    """Top-down merge sort returning a new sorted list.

    Args:
        arr: Input sequence.

    Returns:
        New list with the same elements in ascending order.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quicksort(arr: Sequence[int]) -> list[int]:
    """Functional quicksort using list comprehensions (middle pivot).

    Args:
        arr: Input sequence.

    Returns:
        New sorted list.

    Complexity:
        Time: O(n log n) average, O(n^2) worst case.
        Space: O(n) for new lists.
    """
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def quicksort_inplace(arr: list[int], low: int = 0, high: int | None = None) -> None:
    """In-place quicksort with Lomuto partition + median-of-three.

    Args:
        arr: List to sort in place.
        low: Starting index.
        high: Ending index. If None, defaults to len(arr) - 1.

    Complexity:
        Time: O(n log n) average, O(n^2) worst case.
        Space: O(log n) recursion stack average.
    """
    if high is None:
        high = len(arr) - 1
    while low < high:
        # Median-of-three pivot selection
        mid = (low + high) // 2
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        arr[mid], arr[high] = arr[high], arr[mid]
        pivot = arr[high]

        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        p = i + 1

        # Tail-recurse on smaller side, iterate on larger to limit stack depth
        if p - low < high - p:
            quicksort_inplace(arr, low, p - 1)
            low = p + 1
        else:
            quicksort_inplace(arr, p + 1, high)
            high = p - 1


def closest_pair(points: Sequence[float]) -> float:
    """Closest distance between any two points in 1-D.

    Args:
        points: Sequence of numeric positions on the real line.

    Returns:
        Minimum absolute difference between any pair. ``inf`` if fewer than
        two points.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    n = len(points)
    if n < 2:
        return float("inf")
    sorted_pts = sorted(points)
    return _closest_rec(sorted_pts)


def _closest_rec(sorted_pts: list[float]) -> float:
    n = len(sorted_pts)
    if n <= 3:
        best = float("inf")
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(sorted_pts[i] - sorted_pts[j])
                if d < best:
                    best = d
        return best
    mid = n // 2
    mid_x = sorted_pts[mid]
    d_left = _closest_rec(sorted_pts[:mid])
    d_right = _closest_rec(sorted_pts[mid:])
    d = min(d_left, d_right)
    # Cross-strip: check pairs straddling the midpoint
    left = [x for x in sorted_pts[:mid] if mid_x - x < d]
    right = [x for x in sorted_pts[mid:] if x - mid_x < d]
    # Both lists are sorted, so a linear sweep is enough
    i = j = 0
    while i < len(left) and j < len(right):
        cand = abs(left[i] - right[j])
        if cand < d:
            d = cand
        if left[i] < right[j]:
            i += 1
        else:
            j += 1
    return d


def strassen_matrix_multiply(
    A: list[list[int]], B: list[list[int]]
) -> list[list[int]]:
    """Strassen's recursive matrix multiplication.

    Only works for square matrices whose size is a power of 2.

    Args:
        A: n x n matrix.
        B: n x n matrix.

    Returns:
        n x n product matrix.

    Raises:
        ValueError: If dimensions are non-square or not a power of two.

    Complexity:
        Time: O(n^log2(7)) ~= O(n^2.807). Space: O(n^2).
    """
    n = len(A)
    if n == 0:
        return []
    if any(len(row) != n for row in A) or any(len(row) != n for row in B):
        raise ValueError("Strassen requires square matrices")
    if n & (n - 1) != 0:
        raise ValueError("Strassen requires matrix size to be a power of 2")

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    half = n // 2
    A11 = [row[:half] for row in A[:half]]
    A12 = [row[half:] for row in A[:half]]
    A21 = [row[:half] for row in A[half:]]
    A22 = [row[half:] for row in A[half:]]
    B11 = [row[:half] for row in B[:half]]
    B12 = [row[half:] for row in B[:half]]
    B21 = [row[:half] for row in B[half:]]
    B22 = [row[half:] for row in B[half:]]

    M1 = strassen_matrix_multiply(_add(A11, A22), _add(B11, B22))
    M2 = strassen_matrix_multiply(_add(A21, A22), B11)
    M3 = strassen_matrix_multiply(A11, _sub(B12, B22))
    M4 = strassen_matrix_multiply(A22, _sub(B21, B11))
    M5 = strassen_matrix_multiply(_add(A11, A12), B22)
    M6 = strassen_matrix_multiply(_sub(A21, A11), _add(B11, B12))
    M7 = strassen_matrix_multiply(_sub(A12, A22), _add(B21, B22))

    C11 = _add(_sub(_add(M1, M4), M5), M7)
    C12 = _add(M3, M5)
    C21 = _add(M2, M4)
    C22 = _add(_sub(_add(M1, M3), M2), M6)

    out = [[0] * n for _ in range(n)]
    for i in range(half):
        out[i][:half] = C11[i]
        out[i][half:] = C12[i]
        out[half + i][:half] = C21[i]
        out[half + i][half:] = C22[i]
    return out


def _add(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def _sub(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def karatsuba(x: int, y: int) -> int:
    """Karatsuba multiplication for non-negative integers.

    Args:
        x: First integer.
        y: Second integer.

    Returns:
        x * y.

    Complexity:
        Time: O(n^log2(3)) ~= O(n^1.585). Space: O(log n).
    """
    if x < 0 or y < 0:
        raise ValueError("karatsuba expects non-negative inputs")
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    half = n // 2
    power = 10 ** half

    a, b = divmod(x, power)
    c, d = divmod(y, power)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_bc = karatsuba(a + b, c + d) - ac - bd
    return ac * (10 ** (2 * half)) + ad_bc * power + bd


def find_max(arr: Sequence[int]) -> int:
    """Maximum element via divide-and-conquer.

    Args:
        arr: Non-empty sequence.

    Returns:
        Maximum element.

    Raises:
        ValueError: If empty.

    Complexity:
        Time: O(n). Space: O(log n) recursion.
    """
    if not arr:
        raise ValueError("find_max requires non-empty input")
    return _find_max_rec(arr, 0, len(arr) - 1)


def _find_max_rec(arr: Sequence[int], lo: int, hi: int) -> int:
    if lo == hi:
        return arr[lo]
    mid = (lo + hi) // 2
    left = _find_max_rec(arr, lo, mid)
    right = _find_max_rec(arr, mid + 1, hi)
    return left if left >= right else right


def find_max_min(arr: Sequence[int]) -> tuple[int, int]:
    """Both max and min using ~3n/2 comparisons.

    Args:
        arr: Non-empty sequence.

    Returns:
        (minimum, maximum).

    Raises:
        ValueError: If empty.

    Complexity:
        Time: O(n) with ~3n/2 comparisons. Space: O(log n) recursion.
    """
    if not arr:
        raise ValueError("find_max_min requires non-empty input")
    return _max_min_rec(list(arr), 0, len(arr) - 1)


def _max_min_rec(arr: list[int], lo: int, hi: int) -> tuple[int, int]:
    if lo == hi:
        return arr[lo], arr[lo]
    if hi == lo + 1:
        if arr[lo] <= arr[hi]:
            return arr[lo], arr[hi]
        return arr[hi], arr[lo]
    mid = (lo + hi) // 2
    min1, max1 = _max_min_rec(arr, lo, mid)
    min2, max2 = _max_min_rec(arr, mid + 1, hi)
    return min(min1, min2), max(max1, max2)


def power(base: float, exp: int) -> float:
    """Fast exponentiation (square-and-multiply).

    Args:
        base: The base.
        exp: Non-negative integer exponent.

    Returns:
        ``base ** exp``.

    Raises:
        ValueError: If exp is negative.

    Complexity:
        Time: O(log exp). Space: O(1).
    """
    if exp < 0:
        raise ValueError("exp must be non-negative")
    result = 1.0
    b = base
    e = exp
    while e > 0:
        if e & 1:
            result *= b
        b *= b
        e >>= 1
    return result


def count_inversions(arr: Sequence[int]) -> int:
    """Count inversions in an array (i<j with arr[i]>arr[j]).

    Uses a modified merge sort for O(n log n) time.

    Args:
        arr: Input sequence.

    Returns:
        Number of inversions.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    if len(arr) == 0:
        return 0
    return _count_inv_rec(list(arr), 0, len(arr) - 1)[1]


def _count_inv_rec(arr: list[int], lo: int, hi: int) -> tuple[list[int], int]:
    if lo == hi:
        return [arr[lo]], 0
    mid = (lo + hi) // 2
    left, inv_left = _count_inv_rec(arr, lo, mid)
    right, inv_right = _count_inv_rec(arr, mid + 1, hi)
    merged, inv_cross = _merge_count(left, right)
    return merged, inv_left + inv_right + inv_cross


def _merge_count(left: list[int], right: list[int]) -> tuple[list[int], int]:
    merged: list[int] = []
    i = j = 0
    inv = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inv += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv


__all__ = [
    "merge_sort",
    "quicksort",
    "quicksort_inplace",
    "closest_pair",
    "strassen_matrix_multiply",
    "karatsuba",
    "find_max",
    "find_max_min",
    "power",
    "count_inversions",
]