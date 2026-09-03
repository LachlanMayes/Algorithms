"""Sorting algorithms.

Canonical implementations with full type hints, docstrings, and complexity
notes. Each function either returns a new sorted list or sorts in place
(clearly documented per function).
"""

from __future__ import annotations

from typing import Sequence


def bubble_sort(arr: list[int]) -> list[int]:
    """Bubble sort (in-place). Optimised with early-exit when no swaps.

    Args:
        arr: List to sort in place.

    Returns:
        The same list, sorted in ascending order.

    Complexity:
        Time: O(n^2). Space: O(1). Stable.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: list[int]) -> list[int]:
    """Selection sort (in-place). Always O(n^2); minimal swaps.

    Args:
        arr: List to sort in place.

    Returns:
        The same list, sorted in ascending order.

    Complexity:
        Time: O(n^2). Space: O(1). Not stable.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: list[int]) -> list[int]:
    """Insertion sort (in-place).

    Args:
        arr: List to sort in place.

    Returns:
        The same list, sorted in ascending order.

    Complexity:
        Time: O(n^2). Space: O(1). Stable. Fast on nearly-sorted input.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: Sequence[int]) -> list[int]:
    """Top-down merge sort returning a new sorted list.

    Args:
        arr: Input sequence.

    Returns:
        New sorted list.

    Complexity:
        Time: O(n log n). Space: O(n). Stable.
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
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
    """Functional quicksort with middle pivot (returns a new list).

    Args:
        arr: Input sequence.

    Returns:
        New sorted list.

    Complexity:
        Time: O(n log n) average, O(n^2) worst case.
        Space: O(n).
    """
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def heap_sort(arr: list[int]) -> list[int]:
    """Heap sort (in-place) using a max-heap.

    Args:
        arr: List to sort in place.

    Returns:
        The same list, sorted in ascending order.

    Complexity:
        Time: O(n log n). Space: O(1). Not stable.
    """
    n = len(arr)

    def heapify(start: int, end: int) -> None:
        root = start
        while True:
            child = 2 * root + 1
            if child >= end:
                break
            if child + 1 < end and arr[child + 1] > arr[child]:
                child += 1
            if arr[child] > arr[root]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    # Build max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(i, n)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(0, i)

    return arr


def shell_sort(arr: list[int]) -> list[int]:
    """Shell sort (in-place) with halving gap sequence.

    Args:
        arr: List to sort in place.

    Returns:
        The same list, sorted in ascending order.

    Complexity:
        Time: depends on gap sequence; typically between O(n^1.25) and
            O(n^2). Space: O(1). Not stable.
    """
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


def counting_sort(arr: list[int], max_val: int | None = None) -> list[int]:
    """Counting sort for non-negative integers.

    Args:
        arr: Input list of non-negative integers.
        max_val: Upper bound on values (inclusive). If None, scans the input.

    Returns:
        New sorted list.

    Complexity:
        Time: O(n + k). Space: O(n + k). Stable.
    """
    if not arr:
        return []
    if any(x < 0 for x in arr):
        raise ValueError("counting_sort expects non-negative integers")
    if max_val is None:
        max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    out: list[int] = []
    for value, freq in enumerate(count):
        out.extend([value] * freq)
    return out


def radix_sort(arr: list[int]) -> list[int]:
    """LSD radix sort for non-negative integers (base 10).

    Args:
        arr: List of non-negative integers.

    Returns:
        New sorted list.

    Complexity:
        Time: O(n * d) where d is the number of digits of max value.
        Space: O(n). Stable.
    """
    if not arr:
        return []
    if any(x < 0 for x in arr):
        raise ValueError("radix_sort expects non-negative integers")
    out = list(arr)
    exp = 1
    max_val = max(out)
    while max_val // exp > 0:
        buckets: list[list[int]] = [[] for _ in range(10)]
        for x in out:
            buckets[(x // exp) % 10].append(x)
        out = [x for bucket in buckets for x in bucket]
        exp *= 10
    return out


__all__ = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quicksort",
    "heap_sort",
    "shell_sort",
    "counting_sort",
    "radix_sort",
]