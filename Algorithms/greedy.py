"""Greedy algorithms.

Each function makes locally optimal choices at each step. Greedy algorithms
are not always correct for every problem; the docstrings specify the
preconditions.
"""

from __future__ import annotations

import heapq
from typing import Hashable, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


# Internal Huffman tree node
class _HuffNode:
    __slots__ = ("freq", "char", "left", "right")

    def __init__(
        self,
        freq: float,
        char: Hashable | None = None,
        left: "_HuffNode | None" = None,
        right: "_HuffNode | None" = None,
    ) -> None:
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other: "_HuffNode") -> bool:
        # Python 3 heap comparison tiebreaker
        return self.freq < other.freq


def activity_selection(start: Sequence[int], end: Sequence[int]) -> list[int]:
    """Maximum number of non-overlapping activities (earliest-finish-time).

    Args:
        start: Start time per activity.
        end: End time per activity.

    Returns:
        Indices of the chosen activities (0-indexed positions from the
        input lists).

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    n = len(start)
    if n != len(end):
        raise ValueError("start and end must have the same length")
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: end[i])
    chosen = [order[0]]
    last_end = end[order[0]]
    for idx in order[1:]:
        if start[idx] >= last_end:
            chosen.append(idx)
            last_end = end[idx]
    return chosen


def fractional_knapsack(
    weights: Sequence[float], values: Sequence[float], capacity: float
) -> float:
    """Maximum total value when items can be taken fractionally.

    Args:
        weights: Per-item weights.
        values: Per-item values.
        capacity: Maximum total weight.

    Returns:
        Maximum total value (may be fractional).

    Complexity:
        Time: O(n log n). Space: O(1) extra.
    """
    n = len(weights)
    if n != len(values):
        raise ValueError("weights and values must have the same length")
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    if n == 0 or capacity == 0:
        return 0.0
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    remaining = capacity
    total = 0.0
    for i in order:
        if remaining <= 0:
            break
        take = min(weights[i], remaining)
        total += take * (values[i] / weights[i])
        remaining -= take
    return total


def huffman_coding(
    chars: Sequence[Hashable], freqs: Sequence[float]
) -> dict[Hashable, str]:
    """Build optimal prefix-free Huffman codes.

    Args:
        chars: Symbol per leaf.
        freqs: Frequency per symbol (non-negative).

    Returns:
        Mapping ``{symbol: binary_string_code}``.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    if len(chars) != len(freqs):
        raise ValueError("chars and freqs must have the same length")
    if not chars:
        return {}
    if len(chars) == 1:
        return {chars[0]: "0"}

    heap: list[_HuffNode] = [_HuffNode(f, c) for c, f in zip(chars, freqs)]
    heapq.heapify(heap)

    # Sentinel counter for tie-breaking comparison (chars may not be comparable)
    counter = [0]

    def merge(a: _HuffNode, b: _HuffNode) -> _HuffNode:
        counter[0] += 1
        return _HuffNode(a.freq + b.freq, left=a, right=b)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, merge(left, right))

    codes: dict[Hashable, str] = {}

    def walk(node: _HuffNode, prefix: str) -> None:
        if node.char is not None:
            codes[node.char] = prefix or "0"
            return
        if node.left is not None:
            walk(node.left, prefix + "0")
        if node.right is not None:
            walk(node.right, prefix + "1")

    walk(heap[0], "")
    return codes


def job_sequencing(
    jobs: Sequence[str], deadlines: Sequence[int], profits: Sequence[int]
) -> list[str]:
    """Maximum-profit subset of jobs where each job takes unit time.

    Args:
        jobs: Job identifiers.
        deadlines: Latest-finish deadline per job (1-indexed).
        profits: Profit per job.

    Returns:
        Names of the scheduled jobs (in some order).

    Complexity:
        Time: O(n log n + n * max_deadline). Space: O(n).
    """
    n = len(jobs)
    if not (len(deadlines) == n == len(profits)):
        raise ValueError("jobs, deadlines, profits must have the same length")
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: profits[i], reverse=True)
    max_deadline = max(deadlines)
    if max_deadline < 1:
        return []
    slot: list[str | None] = [None] * (max_deadline + 1)
    scheduled: list[str] = []
    for i in order:
        d = deadlines[i]
        if d <= 0 or d > max_deadline:
            continue
        j = min(d, max_deadline)
        while j > 0:
            if slot[j] is None:
                slot[j] = jobs[i]
                scheduled.append(jobs[i])
                break
            j -= 1
    return scheduled


def minimum_coins(coins: Sequence[int], amount: int) -> int:
    """Minimum coins for ``amount`` using a greedy (largest-first) approach.

    ONLY correct for canonical coin systems (e.g., US {1, 5, 10, 25}). For
    arbitrary denominations, use :func:`dynamic_programming.coin_change`.

    Args:
        coins: Available denominations (positive).
        amount: Target amount.

    Returns:
        Minimum coin count, or ``-1`` if not representable.

    Complexity:
        Time: O(n log n). Space: O(1).
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount == 0:
        return 0
    total = 0
    remaining = amount
    for c in sorted(coins, reverse=True):
        if c <= 0:
            continue
        take, remaining = divmod(remaining, c)
        total += take
    return total if remaining == 0 else -1


def gas_station_circuit(gas: Sequence[int], cost: Sequence[int]) -> int:
    """Starting index for a circular gas-station circuit (or -1).

    At each station i, gain ``gas[i]`` and pay ``cost[i]`` to travel to i+1.

    Args:
        gas: Gas available at each station.
        cost: Gas cost to travel to the next station.

    Returns:
        Index from which a full circuit is possible, or ``-1`` if none.

    Complexity:
        Time: O(n). Space: O(1).
    """
    if len(gas) != len(cost):
        raise ValueError("gas and cost must have the same length")
    if not gas:
        return -1
    total = 0
    tank = 0
    start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


__all__ = [
    "activity_selection",
    "fractional_knapsack",
    "huffman_coding",
    "job_sequencing",
    "minimum_coins",
    "gas_station_circuit",
]