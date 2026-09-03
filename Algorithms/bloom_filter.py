"""Bloom filter and related probabilistic data structures.

Reference: arXiv:2401.02647 - "Technical Report: Modeling Average False
Positive Rates of Recycling Bloom Filters" (Dozier, Salamatian, Rubenstein).

A Bloom filter is a space-efficient probabilistic data structure that
answers "is this element in the set?" with possible false positives but
never false negatives. It uses k hash functions and a bit array of
size m.
"""

from __future__ import annotations

import hashlib
from typing import Iterable


class BloomFilter:
    """Standard Bloom filter for set membership testing.

    Args:
        capacity: Expected number of elements to insert.
        error_rate: Target false-positive probability (e.g. 0.01 for 1%).

    Raises:
        ValueError: If parameters are invalid.

    Complexity:
        insert / __contains__: O(k) where k is the number of hash functions.
        Space: O(m) bits where m is derived from capacity and error_rate.
    """

    def __init__(self, capacity: int, error_rate: float = 0.01) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate must be in (0, 1)")
        # Optimal m and k per Bloom (1970). m = -n*ln(p) / (ln 2)^2, k = (m/n)*ln 2.
        import math
        ln2 = math.log(2)
        m = math.ceil(-(capacity * math.log(error_rate)) / (ln2 ** 2))
        k = max(1, round((m / capacity) * ln2))
        self._m = m
        self._k = k
        self._bits = bytearray(m)
        self._count = 0

    def _hashes(self, item: bytes) -> list[int]:
        """Generate k distinct hash positions using SHA-256 double hashing.

        Uses the technique of deriving two independent 64-bit hashes (h1, h2)
        from SHA-256, then generating h_i = (h1 + i*h2) mod m for i in [0, k).
        """
        digest = hashlib.sha256(item).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big")
        return [(h1 + i * h2) % self._m for i in range(self._k)]

    def add(self, item: str | bytes) -> None:
        """Insert an item into the filter.

        Args:
            item: Item to add. Strings are encoded as UTF-8.
        """
        data = item.encode("utf-8") if isinstance(item, str) else item
        for pos in self._hashes(data):
            self._bits[pos] = 1
        self._count += 1

    def __contains__(self, item: str | bytes) -> bool:
        """Check whether ``item`` *might* be in the filter.

        Returns False if certainly not present; True if possibly present
        (with probability up to the configured ``error_rate``).
        """
        data = item.encode("utf-8") if isinstance(item, str) else item
        return all(self._bits[pos] for pos in self._hashes(data))

    @property
    def size_bits(self) -> int:
        """Number of bits in the underlying array."""
        return self._m

    @property
    def num_hashes(self) -> int:
        """Number of hash functions (k)."""
        return self._k

    @property
    def count(self) -> int:
        """Number of items inserted (approximate; multiple adds of the same
        item are not deduplicated)."""
        return self._count

    def fill_ratio(self) -> float:
        """Fraction of bits set to 1."""
        if self._m == 0:
            return 0.0
        return sum(self._bits) / self._m

    def estimated_false_positive_rate(self) -> float:
        """Current theoretical false-positive rate given the fill ratio.

        For optimal k, this is ``(1 - e^(-k*n/m))^k`` where n is the count.
        """
        import math
        n = self._count
        if n == 0:
            return 0.0
        exponent = -self._k * n / self._m
        return (1 - math.exp(exponent)) ** self._k


class CountingBloomFilter:
    """Counting Bloom filter - supports deletion at the cost of 4x space.

    Each cell stores a small counter instead of a single bit. Removes
    decrement the counters; deletes are only allowed when the item was
    previously inserted.

    Complexity:
        add / remove / __contains__: O(k). Space: O(m * 4) bytes.
    """

    def __init__(self, capacity: int, error_rate: float = 0.01) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate must be in (0, 1)")
        import math
        ln2 = math.log(2)
        m = math.ceil(-(capacity * math.log(error_rate)) / (ln2 ** 2))
        k = max(1, round((m / capacity) * ln2))
        self._m = m
        self._k = k
        self._counters = [0] * m
        self._count = 0

    def _hashes(self, item: bytes) -> list[int]:
        digest = hashlib.sha256(item).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big")
        return [(h1 + i * h2) % self._m for i in range(self._k)]

    def add(self, item: str | bytes) -> None:
        data = item.encode("utf-8") if isinstance(item, str) else item
        for pos in self._hashes(data):
            self._counters[pos] += 1
        self._count += 1

    def remove(self, item: str | bytes) -> bool:
        """Decrement counters. Returns False if item probably wasn't present.

        Args:
            item: Item to remove.
        """
        data = item.encode("utf-8") if isinstance(item, str) else item
        positions = self._hashes(data)
        if any(self._counters[p] == 0 for p in positions):
            return False
        for pos in positions:
            self._counters[pos] -= 1
        self._count -= 1
        return True

    def __contains__(self, item: str | bytes) -> bool:
        data = item.encode("utf-8") if isinstance(item, str) else item
        return all(self._counters[p] > 0 for p in self._hashes(data))

    @property
    def size(self) -> int:
        return self._m

    @property
    def count(self) -> int:
        return self._count


__all__ = ["BloomFilter", "CountingBloomFilter"]