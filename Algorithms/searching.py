"""Searching algorithms.

This module provides implementations of common searching algorithms with full
type hints, docstrings, and complexity notes.

All functions operate on sequences (lists/tuples) and return the index of the
target element, or -1 if not found. For algorithms that require sorted input,
the caller is responsible for passing a sorted sequence.
"""

from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")


def linear_search(arr: Sequence[T], target: T) -> int:
    """Sequential search over an arbitrary sequence.

    Args:
        arr: The sequence to search.
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(n). Space: O(1).
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr: Sequence[T], target: T) -> int:
    """Iterative binary search over a sorted sequence.

    Args:
        arr: A sorted sequence (ascending).
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(log n). Space: O(1).
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(
    arr: Sequence[T], target: T, lo: int = 0, hi: int | None = None
) -> int:
    """Recursive binary search over a sorted sequence.

    Args:
        arr: A sorted sequence (ascending).
        target: The element to look for.
        lo: Lower bound index (inclusive).
        hi: Upper bound index (inclusive). If None, defaults to len(arr)-1.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(log n). Space: O(log n) recursion stack.
    """
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    return binary_search_recursive(arr, target, lo, mid - 1)


def ternary_search(arr: Sequence[T], target: T) -> int:
    """Ternary search over a sorted sequence.

    Splits the array into three parts at each step.

    Args:
        arr: A sorted sequence (ascending).
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(log_3 n). Space: O(1). (Slightly more comparisons than binary search.)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        third = (hi - lo) // 3
        m1 = lo + third
        m2 = hi - third
        if arr[m1] == target:
            return m1
        if arr[m2] == target:
            return m2
        if target < arr[m1]:
            hi = m1 - 1
        elif target > arr[m2]:
            lo = m2 + 1
        else:
            lo, hi = m1 + 1, m2 - 1
    return -1


def jump_search(arr: Sequence[T], target: T) -> int:
    """Jump search over a sorted sequence.

    Jumps ahead by sqrt(n) blocks, then performs a linear search within
    the identified block.

    Args:
        arr: A sorted sequence (ascending).
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(sqrt(n)). Space: O(1).
    """
    n = len(arr)
    if n == 0:
        return -1
    step = max(1, int(n ** 0.5))
    prev = 0
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return -1


def interpolation_search(arr: Sequence[int], target: int) -> int:
    """Interpolation search on a sorted, uniformly distributed numeric sequence.

    Estimates the position of ``target`` based on its value relative to the
    endpoints of the current search window.

    Args:
        arr: A sorted sequence of numbers (ascending).
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(log(log n)) average, O(n) worst case (non-uniform data).
        Space: O(1).
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if lo == hi:
            if arr[lo] == target:
                return lo
            return -1
        # Avoid division by zero on duplicate values
        if arr[hi] == arr[lo]:
            if arr[lo] == target:
                return lo
            return -1
        pos = lo + ((target - arr[lo]) * (hi - lo)) // (arr[hi] - arr[lo])
        if pos < lo or pos > hi:
            return -1
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def exponential_search(arr: Sequence[T], target: T) -> int:
    """Exponential (galloping) search followed by binary search.

    Finds a range [lo, hi] where the target may exist by doubling the index,
    then performs binary search inside that range.

    Args:
        arr: A sorted sequence (ascending).
        target: The element to look for.

    Returns:
        The index of ``target`` in ``arr``, or -1 if not found.

    Complexity:
        Time: O(log n). Space: O(1).
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    i = 1
    while i < n and arr[i] <= target:
        i *= 2
    return binary_search_recursive(arr, target, i // 2, min(i, n - 1))


__all__ = [
    "linear_search",
    "binary_search",
    "binary_search_recursive",
    "ternary_search",
    "jump_search",
    "interpolation_search",
    "exponential_search",
]