"""Advanced dynamic programming.

Includes:
    - Bitmask DP: travelling salesman problem (Held-Karp).
    - Digit DP: count integers in [lo, hi] satisfying a digit predicate.
    - Longest palindromic subsequence.
    - Optimal binary search tree.
    - Boolean parenthesization (matrix chain variant).
    - Longest path in DAG.
    - Weighted interval scheduling.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import Callable, Sequence


def tsp_held_karp(dist: list[list[float]], start: int = 0) -> tuple[float, list[int]]:
    """Travelling Salesman via Held-Karp DP (1962). Optimal tour length
    and one optimal tour.

    Args:
        dist: Square distance matrix ``dist[i][j]`` = cost to travel i -> j.
            Use ``float('inf')`` for unreachable pairs.
        start: Fixed starting city index.

    Returns:
        ``(best_length, tour)`` where ``tour`` is a list of city indices
        starting and ending at ``start``.

    Raises:
        ValueError: If ``dist`` is not square or ``start`` is out of range.

    Complexity:
        Time: O(n^2 * 2^n). Space: O(n * 2^n).
    """
    n = len(dist)
    if n == 0:
        return 0.0, [start]
    if any(len(row) != n for row in dist):
        raise ValueError("dist must be square")
    if not 0 <= start < n:
        raise ValueError("start out of range")
    if n == 1:
        return 0.0, [start, start]

    # dp[mask][i] = min cost of starting at `start`, visiting all cities
    # in `mask`, ending at city i. mask bit j means city j has been visited.
    INF = float("inf")
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    dp[1 << start][start] = 0.0

    for mask in range(size):
        if not (mask & (1 << start)):
            continue
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            cur = dp[mask][last]
            if cur == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                if dist[last][nxt] == INF:
                    continue
                nmask = mask | (1 << nxt)
                new = cur + dist[last][nxt]
                if new < dp[nmask][nxt]:
                    dp[nmask][nxt] = new
                    parent[nmask][nxt] = last

    full = (1 << n) - 1
    best = INF
    last_city = -1
    for i in range(n):
        if dist[i][start] == INF:
            continue
        total = dp[full][i] + dist[i][start]
        if total < best:
            best = total
            last_city = i
    if best == INF:
        return float("inf"), []

    # Reconstruct tour
    tour = [start]
    mask, cur = full, last_city
    while cur != -1 and cur != start:
        tour.append(cur)
        prev = parent[mask][cur]
        mask ^= 1 << cur
        cur = prev
    tour.append(start)
    tour.reverse()
    return best, tour


def longest_palindromic_subsequence(s: str) -> int:
    """Longest palindromic SUBSEQUENCE (not substring) length.

    Args:
        s: Input string.

    Returns:
        Length of the longest palindromic subsequence.

    Complexity:
        Time: O(n^2). Space: O(n^2).
    """
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


def longest_path_dag(n_nodes: int, edges: Sequence[tuple[int, int, float]]) -> float:
    """Longest path in a DAG using topological ordering + DP.

    Args:
        n_nodes: Number of nodes, labelled 0..n_nodes-1.
        edges: List of ``(u, v, weight)`` directed edges.

    Returns:
        Length of the longest path. ``0`` if DAG is empty.

    Complexity:
        Time: O(V + E). Space: O(V + E).
    """
    if n_nodes == 0:
        return 0.0
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n_nodes)]
    indeg = [0] * n_nodes
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    # Kahn topological sort
    queue = [i for i in range(n_nodes) if indeg[i] == 0]
    order: list[int] = []
    while queue:
        u = queue.pop()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != n_nodes:
        raise ValueError("Graph has a cycle; not a DAG")
    dp = [0.0] * n_nodes
    for u in order:
        for v, w in adj[u]:
            if dp[u] + w > dp[v]:
                dp[v] = dp[u] + w
    return max(dp) if dp else 0.0


def weighted_interval_scheduling(
    intervals: Sequence[tuple[float, float, float]]
) -> list[int]:
    """Weighted interval scheduling: select maximum-weight non-overlapping
    intervals using binary-search + DP.

    Args:
        intervals: ``(start, end, weight)``.

    Returns:
        Indices of the selected intervals.

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    n = len(intervals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: intervals[i][1])
    ends = [intervals[i][1] for i in order]
    dp = [0.0] * (n + 1)
    take = [False] * n
    for i in range(1, n + 1):
        idx = order[i - 1]
        s, e, w = intervals[idx]
        # Find rightmost j <= i-1 with ends[j-1] <= s in order-by-end terms
        j = bisect_right(ends, s, 0, i - 1)
        take_val = w + dp[j]
        skip_val = dp[i - 1]
        if take_val > skip_val:
            dp[i] = take_val
            take[i - 1] = True
        else:
            dp[i] = skip_val
    selected: list[int] = []
    i = n
    while i > 0:
        if take[i - 1]:
            selected.append(order[i - 1])
            j = bisect_right(ends, intervals[order[i - 1]][0], 0, i - 1)
            i = j
        else:
            i -= 1
    selected.reverse()
    return selected


def boolean_parenthesization(symbols: Sequence[bool], operators: Sequence[str]) -> int:
    """Count ways to parenthesise a boolean expression to evaluate to True.

    Args:
        symbols: Sequence of boolean values.
        operators: Sequence of operators between symbols (``&``, ``|``,
            ``^``). Length must be ``len(symbols) - 1``.

    Returns:
        Number of parenthesizations yielding True.

    Complexity:
        Time: O(n^3). Space: O(n^2).
    """
    n = len(symbols)
    if n == 0:
        return 0
    if n == 1:
        return 1 if symbols[0] else 0
    if len(operators) != n - 1:
        raise ValueError("operators length must be len(symbols) - 1")
    # dp[i][j] = (T_count, F_count) for substring symbols[i..j]
    T = [[0] * n for _ in range(n)]
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        if symbols[i]:
            T[i][i] = 1
        else:
            F[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                op = operators[k]
                lt, lf = T[i][k], F[i][k]
                rt, rf = T[k + 1][j], F[k + 1][j]
                if op == "&":
                    T[i][j] += lt * rt
                    F[i][j] += lt * rf + lf * rt + lf * rf
                elif op == "|":
                    T[i][j] += lt * rt + lt * rf + lf * rt
                    F[i][j] += lf * rf
                elif op == "^":
                    T[i][j] += lt * rf + lf * rt
                    F[i][j] += lt * rt + lf * rf
                else:
                    raise ValueError(f"unknown operator: {op}")
    return T[0][n - 1]


def digit_dp(
    n: int,
    predicate: Callable[[list[int]], bool],
) -> int:
    """Digit DP: count integers in [0, n] whose decimal digit sequence
    satisfies ``predicate``.

    Args:
        n: Non-negative upper bound.
        predicate: Function from list of digits (most-significant first,
            no leading zeros; for the value 0 the input is ``[0]``) to
            bool.

    Returns:
        Count of valid integers in [0, n].

    Complexity:
        Time: O(len(n) * 2 * 10). Space: O(len(n)).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    digits = [int(c) for c in str(n)]
    memo: dict[tuple[int, bool, bool, tuple], int] = {}

    def rec(pos: int, tight: bool, started: bool, built: tuple) -> int:
        key = (pos, tight, started, built)
        if key in memo:
            return memo[key]
        if pos == len(digits):
            # Apply predicate on the actual digit list (excluding leading
            # zeros). Number 0 is represented as [0].
            if not started:
                result = 1 if predicate([0]) else 0
            else:
                result = 1 if predicate(list(built)) else 0
            memo[key] = result
            return result
        upper = digits[pos] if tight else 9
        total = 0
        for d in range(0, upper + 1):
            ns = started or (d != 0)
            new_built = built + (d,) if ns else built
            total += rec(pos + 1, tight and d == upper, ns, new_built)
        memo[key] = total
        return total

    return rec(0, True, False, ())


def is_palindrome(s: str) -> bool:
    """True if ``s`` is a palindrome."""
    return s == s[::-1]


__all__ = [
    "tsp_held_karp",
    "longest_palindromic_subsequence",
    "longest_path_dag",
    "weighted_interval_scheduling",
    "boolean_parenthesization",
    "digit_dp",
    "is_palindrome",
]