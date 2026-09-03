"""Randomized algorithms.

Includes:
    - Reservoir sampling (Vitter): sample k items uniformly from a stream.
    - Fisher-Yates shuffle.
    - Random quickselect (Hoare's selection).
    - Miller-Rabin primality test (randomised).
    - Random BST (Treap).
    - Monte Carlo pi estimation.
"""

from __future__ import annotations

import math
import random
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


def reservoir_sample(stream: Sequence[T] | "Iterable[T]", k: int, seed: int | None = None) -> list[T]:
    """Reservoir sampling (Algorithm R, Vitter 1985): uniformly sample k
    items from a stream of unknown length.

    Args:
        stream: Any iterable (may be a generator).
        k: Sample size.
        seed: Optional random seed.

    Returns:
        List of k uniformly sampled items (sampling without replacement).

    Complexity:
        Time: O(n) where n = len(stream). Space: O(k).
    """
    if k <= 0:
        return []
    rng = random.Random(seed)
    reservoir: list[T] = []
    it = iter(stream)
    for i, x in enumerate(it):
        if i < k:
            reservoir.append(x)
        else:
            j = rng.randint(0, i)
            if j < k:
                reservoir[j] = x  # type: ignore[assignment]
    return reservoir


def fisher_yates_shuffle(arr: list[T], seed: int | None = None) -> list[T]:
    """In-place Fisher-Yates shuffle (in-place variant returns None; this
    returns a new shuffled list).

    Args:
        arr: Input list.
        seed: Optional random seed.

    Returns:
        New list with the same elements in uniformly random order.

    Complexity:
        Time: O(n). Space: O(n).
    """
    rng = random.Random(seed)
    out = list(arr)
    for i in range(len(out) - 1, 0, -1):
        j = rng.randint(0, i)
        out[i], out[j] = out[j], out[i]
    return out


def quickselect(arr: Sequence[T], k: int, seed: int | None = None) -> T:
    """Quickselect: find the k-th smallest element (0-indexed) in O(n)
    expected time (Hoare 1961).

    Args:
        arr: Non-empty sequence.
        k: 0-indexed rank (0 = smallest).
        seed: Optional random seed for pivot choice.

    Returns:
        The k-th smallest element.

    Raises:
        ValueError: If ``arr`` is empty or k is out of range.

    Complexity:
        Time: O(n) expected, O(n^2) worst case. Space: O(1) tail recursion.
    """
    if not arr:
        raise ValueError("arr must be non-empty")
    if not 0 <= k < len(arr):
        raise ValueError(f"k out of range: {k}")
    rng = random.Random(seed)
    data = list(arr)
    lo, hi = 0, len(data) - 1
    while lo < hi:
        # Random pivot (Lomuto partition)
        pivot_idx = rng.randint(lo, hi)
        pivot = data[pivot_idx]
        data[pivot_idx], data[hi] = data[hi], data[pivot_idx]
        i = lo
        for j in range(lo, hi):
            if data[j] < pivot:
                data[i], data[j] = data[j], data[i]
                i += 1
        data[i], data[hi] = data[hi], data[i]
        if k == i:
            return data[i]
        if k < i:
            hi = i - 1
        else:
            lo = i + 1
    return data[lo]


def miller_rabin(n: int, witnesses: Sequence[int] | None = None, seed: int | None = None) -> bool:
    """Miller-Rabin primality test (randomised).

    For n < 3,317,044,800,329,073,969, deterministic witnesses
    {2,3,5,7,11,13,17,19,23,29,31,37} are sufficient. Default to those.

    Args:
        n: Integer to test.
        witnesses: Optional list of bases to use.
        seed: Optional seed for random witness selection.

    Returns:
        True if ``n`` is probably prime (no false negatives; possibly
        false positive with prob < 4^(-k)).

    Raises:
        ValueError: If n <= 1.

    Complexity:
        Time: O(k * log^3 n). Space: O(1).
    """
    if n <= 1:
        raise ValueError("n must be >= 2")
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    rng = random.Random(seed)
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if witnesses is None:
        witnesses = small_primes
    # Filter to bases < n and gcd=1
    bases = [a for a in witnesses if 2 <= a < n and math.gcd(a, n) == 1]
    if not bases:
        # Random witnesses
        for _ in range(8):
            a = rng.randrange(2, n - 1)
            bases.append(a)

    # Write n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def monte_carlo_pi(samples: int = 100_000, seed: int | None = None) -> float:
    """Estimate pi by sampling uniform points in the unit square and counting
    the fraction that lie inside the unit circle.

    Args:
        samples: Number of random samples.
        seed: Optional random seed.

    Returns:
        Estimated value of pi.

    Complexity:
        Time: O(samples). Space: O(1).
    """
    if samples <= 0:
        raise ValueError("samples must be positive")
    rng = random.Random(seed)
    inside = 0
    for _ in range(samples):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / samples


# --------------------------------------------------------------------------- #
# Treap (randomised BST)
# --------------------------------------------------------------------------- #


class _TreapNode(Generic[T]):
    __slots__ = ("key", "value", "priority", "left", "right")

    def __init__(self, key: int, value: T) -> None:
        self.key = key
        self.value = value
        self.priority = random.random()
        self.left: "_TreapNode[T] | None" = None
        self.right: "_TreapNode[T] | None" = None


class Treap(Generic[T]):
    """Treap: a randomised BST where each node has a random priority;
    heap-ordered by priority, BST-ordered by key.

    Provides expected O(log n) insert / search / delete.

    Args:
        seed: Optional seed for reproducible priorities.
    """

    def __init__(self, seed: int | None = None) -> None:
        self._root: _TreapNode[T] | None = None
        if seed is not None:
            random.seed(seed)

    def _rotate_right(self, y: _TreapNode[T]) -> _TreapNode[T]:
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(self, x: _TreapNode[T]) -> _TreapNode[T]:
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _insert(self, node: _TreapNode[T] | None, key: int, value: T) -> _TreapNode[T]:
        if node is None:
            return _TreapNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
            if node.left.priority < node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
            if node.right.priority < node.priority:
                node = self._rotate_left(node)
        else:
            node.value = value
        return node

    def insert(self, key: int, value: T) -> None:
        self._root = self._insert(self._root, key, value)

    def _delete(self, node: _TreapNode[T] | None, key: int) -> _TreapNode[T] | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
            return node
        if key > node.key:
            node.right = self._delete(node.right, key)
            return node
        # key == node.key
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        if node.left.priority < node.right.priority:
            node = self._rotate_right(node)
            node.right = self._delete(node.right, key)
        else:
            node = self._rotate_left(node)
            node.left = self._delete(node.left, key)
        return node

    def delete(self, key: int) -> bool:
        prev = self._root
        self._root = self._delete(self._root, key)
        return self._root is not prev or prev is not None and prev.key != key

    def search(self, key: int) -> T | None:
        node = self._root
        while node is not None:
            if key == node.key:
                return node.value
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def __contains__(self, key: int) -> bool:
        return self.search(key) is not None


__all__ = [
    "reservoir_sample",
    "fisher_yates_shuffle",
    "quickselect",
    "miller_rabin",
    "monte_carlo_pi",
    "Treap",
]