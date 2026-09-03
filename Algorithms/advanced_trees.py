"""Advanced tree data structures: Segment Tree, Fenwick Tree (BIT), Skip List.

These are workhorses for range queries and ordered-set operations.

References:
    - Fenwick, P. M. (1994). "A new data structure for cumulative frequency
      tables". Software: Practice and Experience.
    - Pugh, W. (1990). "Skip lists: a probabilistic alternative to balanced
      trees". Communications of the ACM.
    - Tarjan, R. E. (1987). "An O(log n) algorithm for longest common
      subsequences". (segment tree predecessors)
"""

from __future__ import annotations

import random
from typing import Generic, Iterable, Sequence, TypeVar

T = TypeVar("T")


# --------------------------------------------------------------------------- #
# Segment Tree
# --------------------------------------------------------------------------- #


class SegmentTree(Generic[T]):
    """Segment tree supporting range queries and point updates.

    Uses an arbitrary associative function ``combine`` and an ``identity``
    element. Build time O(n), range query O(log n), point update O(log n).

    Examples:
        Range sum query::

            st = SegmentTree([1, 3, 5, 7, 9], combine=lambda a, b: a + b,
                             identity=0)
            st.query(1, 3)  # -> 3 + 5 + 7 = 15
            st.update(1, 10)  # arr becomes [1, 10, 5, 7, 9]
            st.query(1, 3)  # -> 10 + 5 + 7 = 22

        Range minimum query::

            st = SegmentTree([3, 1, 4, 1, 5, 9, 2, 6], combine=min,
                             identity=float('inf'))
            st.query(2, 5)  # -> 1
    """

    def __init__(
        self,
        data: Iterable[T],
        combine: "callable[[T, T], T]",
        identity: T,
    ) -> None:
        self._combine = combine
        self._identity = identity
        self._data: list[T] = list(data)
        self._n = len(self._data)
        if self._n == 0:
            self._tree = []
            return
        self._tree = [identity] * (2 * self._n)
        for i in range(self._n):
            self._tree[self._n + i] = self._data[i]
        for i in range(self._n - 1, 0, -1):
            self._tree[i] = combine(self._tree[2 * i], self._tree[2 * i + 1])

    def update(self, index: int, value: T) -> None:
        """Set element at ``index`` to ``value``. O(log n).

        Args:
            index: 0-based position.
            value: New value.
        """
        if not 0 <= index < self._n:
            raise IndexError(f"index {index} out of range")
        i = self._n + index
        self._tree[i] = value
        self._data[index] = value
        i //= 2
        while i >= 1:
            self._tree[i] = self._combine(self._tree[2 * i], self._tree[2 * i + 1])
            i //= 2

    def query(self, left: int, right: int) -> T:
        """Combine elements in ``[left, right]`` (inclusive). O(log n).

        Args:
            left: 0-based inclusive left bound.
            right: 0-based inclusive right bound.
        """
        if self._n == 0:
            return self._identity
        if not 0 <= left <= right < self._n:
            raise IndexError(f"invalid range [{left}, {right}]")
        l = left + self._n
        r = right + self._n
        result = self._identity
        while l <= r:
            if l % 2 == 1:
                result = self._combine(result, self._tree[l])
                l += 1
            if r % 2 == 0:
                result = self._combine(result, self._tree[r])
                r -= 1
            l //= 2
            r //= 2
        return result

    def __len__(self) -> int:
        return self._n


# --------------------------------------------------------------------------- #
# Fenwick Tree (Binary Indexed Tree)
# --------------------------------------------------------------------------- #


class FenwickTree:
    """Fenwick tree / Binary Indexed Tree for prefix queries and point updates.

    Supports:
        - ``update(i, delta)``: add delta to position i. O(log n).
        - ``query(i)``: prefix sum of positions[0..i]. O(log n).
        - ``range_query(l, r)``: sum of positions[l..r]. O(log n).

    Args:
        size: Number of elements (initialised to zero).
        values: Optional initial values (length n). If provided, ``size`` is
            ignored.
    """

    def __init__(self, size: int = 0, values: Iterable[int] | None = None) -> None:
        if values is not None:
            self._n = len(list(values))
            self._bit = [0] * (self._n + 1)
            for i, v in enumerate(values):
                self._add(i + 1, v)
        else:
            if size < 0:
                raise ValueError("size must be non-negative")
            self._n = size
            self._bit = [0] * (size + 1)

    def _add(self, i: int, delta: int) -> None:
        """1-indexed internal add."""
        while i <= self._n:
            self._bit[i] += delta
            i += i & -i

    def _sum(self, i: int) -> int:
        """1-indexed internal prefix sum."""
        s = 0
        while i > 0:
            s += self._bit[i]
            i -= i & -i
        return s

    def update(self, index: int, delta: int) -> None:
        """Add ``delta`` to position ``index``. O(log n).

        Args:
            index: 0-based position.
            delta: Signed integer to add.
        """
        if not 0 <= index < self._n:
            raise IndexError(f"index {index} out of range")
        self._add(index + 1, delta)

    def set(self, index: int, value: int) -> None:
        """Set position ``index`` to ``value`` (not increment). O(log n).

        Args:
            index: 0-based position.
            value: New value.
        """
        if not 0 <= index < self._n:
            raise IndexError(f"index {index} out of range")
        current = self.query(index)
        if index > 0:
            current -= self._sum(index)  # already returns sum up to index
        # Recompute properly
        current = self._sum(index + 1) - self._sum(index)
        self._add(index + 1, value - current)

    def query(self, index: int) -> int:
        """Prefix sum ``[0..index]`` (inclusive). O(log n).

        Args:
            index: 0-based inclusive right bound.
        """
        if not 0 <= index < self._n:
            raise IndexError(f"index {index} out of range")
        return self._sum(index + 1)

    def range_query(self, left: int, right: int) -> int:
        """Sum over ``[left, right]`` inclusive. O(log n)."""
        if not 0 <= left <= right < self._n:
            raise IndexError(f"invalid range [{left}, {right}]")
        if left == 0:
            return self._sum(right + 1)
        return self._sum(right + 1) - self._sum(left)

    def __len__(self) -> int:
        return self._n


# --------------------------------------------------------------------------- #
# Skip List (clean reimplementation)
# --------------------------------------------------------------------------- #


class _SkipNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T | None = None, level: int = 1) -> None:
        self.value: T | None = value
        # next[i] is the successor at level i (0-indexed).
        self.next: list[_SkipNode[T] | None] = [None] * level


class SkipList(Generic[T]):
    """Probabilistic skip list for ordered sets. Provides expected O(log n)
    search / insert / delete via random level promotion (Pugh 1990).

    Args:
        max_level: Maximum number of levels. Default 32 (supports up to
            ~4 billion elements).
        p: Promotion probability. Default 0.5 (the standard choice).
        seed: Optional random seed for reproducibility.
    """

    def __init__(
        self,
        max_level: int = 32,
        p: float = 0.5,
        seed: int | None = None,
    ) -> None:
        if max_level <= 0:
            raise ValueError("max_level must be positive")
        if not 0 < p < 1:
            raise ValueError("p must be in (0, 1)")
        self._max_level = max_level
        self._p = p
        self._level = 0
        self._head: _SkipNode[T] = _SkipNode[T](level=max_level)
        self._size = 0
        self._rng = random.Random(seed)

    def _random_level(self) -> int:
        lvl = 0
        while self._rng.random() < self._p and lvl < self._max_level - 1:
            lvl += 1
        return lvl

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: T) -> bool:
        node = self._head
        for i in range(self._level, -1, -1):
            nxt = node.next[i]
            while nxt is not None and nxt.value < value:
                node = nxt
                nxt = node.next[i]
        nxt = node.next[0]
        return nxt is not None and nxt.value == value

    def add(self, value: T) -> None:
        """Insert ``value``. Expected O(log n). Duplicates are ignored."""
        update: list[_SkipNode[T]] = [self._head] * self._max_level
        node = self._head
        for i in range(self._level, -1, -1):
            nxt = node.next[i]
            while nxt is not None and nxt.value < value:
                node = nxt
                nxt = node.next[i]
            update[i] = node

        if node.next[0] is not None and node.next[0].value == value:
            return  # duplicate

        new_level = self._random_level()
        if new_level > self._level:
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._head
            self._level = new_level

        new_node: _SkipNode[T] = _SkipNode[T](value, level=new_level + 1)
        for i in range(new_level + 1):
            new_node.next[i] = update[i].next[i]
            update[i].next[i] = new_node
        self._size += 1

    def discard(self, value: T) -> bool:
        """Remove ``value`` if present. Returns True if removed."""
        update: list[_SkipNode[T]] = [self._head] * self._max_level
        node = self._head
        for i in range(self._level, -1, -1):
            nxt = node.next[i]
            while nxt is not None and nxt.value < value:
                node = nxt
                nxt = node.next[i]
            update[i] = node

        target = node.next[0]
        if target is None or target.value != value:
            return False
        for i in range(self._level + 1):
            if update[i].next[i] is target:
                update[i].next[i] = target.next[i]
        while self._level > 0 and self._head.next[self._level] is None:
            self._level -= 1
        self._size -= 1
        return True

    def to_list(self) -> list[T]:
        """Return all values in sorted order."""
        out: list[T] = []
        node = self._head.next[0]
        while node is not None:
            out.append(node.value)  # type: ignore[arg-type]
            node = node.next[0]
        return out


__all__ = ["SegmentTree", "FenwickTree", "SkipList"]