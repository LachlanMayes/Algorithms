"""Dynamic programming algorithms.

Each function uses memoization or tabulation. Time/space complexities are
documented per function.
"""

from __future__ import annotations

from typing import Sequence


def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """Fibonacci number F(n) using memoized recursion.

    Args:
        n: Non-negative integer index.
        memo: Optional pre-existing memo dict (used by recursion).

    Returns:
        F(n) where F(0) = 0, F(1) = 1.

    Raises:
        ValueError: If n is negative.

    Complexity:
        Time: O(n). Space: O(n).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        memo[n] = n
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tab(n: int) -> int:
    """Fibonacci number F(n) using bottom-up tabulation.

    Args:
        n: Non-negative integer index.

    Returns:
        F(n).

    Raises:
        ValueError: If n is negative.

    Complexity:
        Time: O(n). Space: O(1) (rolling variables).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def coin_change(coins: Sequence[int], amount: int) -> int:
    """Minimum number of coins to make ``amount``.

    Args:
        coins: Available coin denominations (assumed non-negative).
        amount: Target amount (non-negative).

    Returns:
        Minimum coins needed, or ``-1`` if impossible.

    Complexity:
        Time: O(amount * len(coins)). Space: O(amount).
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    max_val = amount + 1
    dp = [max_val] * max_val
    dp[0] = 0
    for x in range(1, amount + 1):
        for c in coins:
            if c <= 0:
                continue
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
    return dp[amount] if dp[amount] != max_val else -1


def longest_common_subsequence(s1: str, s2: str) -> int:
    """Length of the longest common subsequence (LCS).

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Length of the LCS.

    Complexity:
        Time: O(len(s1) * len(s2)). Space: O(min(len(s1), len(s2))).
    """
    m, n = len(s1), len(s2)
    if m < n:
        s1, s2, m, n = s2, s1, n, m
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        c1 = s1[i - 1]
        for j in range(1, n + 1):
            if c1 == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    return prev[n]


def longest_common_substring(s1: str, s2: str) -> int:
    """Length of the longest contiguous common substring.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Length of the longest common substring.

    Complexity:
        Time: O(len(s1) * len(s2)). Space: O(min(len(s1), len(s2))).
    """
    m, n = len(s1), len(s2)
    if m < n:
        s1, s2, m, n = s2, s1, n, m
    prev = [0] * (n + 1)
    best = 0
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        c1 = s1[i - 1]
        for j in range(1, n + 1):
            if c1 == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
                if curr[j] > best:
                    best = curr[j]
        prev = curr
    return best


def edit_distance(s1: str, s2: str) -> int:
    """Levenshtein edit distance (insert / delete / substitute).

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Minimum number of edits to transform ``s1`` into ``s2``.

    Complexity:
        Time: O(len(s1) * len(s2)). Space: O(min(len(s1), len(s2))).
    """
    m, n = len(s1), len(s2)
    if m < n:
        s1, s2, m, n = s2, s1, n, m
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
        prev, curr = curr, prev
    return prev[n]


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """0/1 knapsack: max total value with at most ``capacity`` weight.

    Each item may be picked at most once.

    Args:
        weights: Per-item weights.
        values: Per-item values.
        capacity: Maximum total weight.

    Returns:
        Maximum total value achievable.

    Complexity:
        Time: O(n * capacity). Space: O(capacity).
    """
    n = len(weights)
    if n != len(values):
        raise ValueError("weights and values must have the same length")
    dp = [0] * (capacity + 1)
    for i in range(n):
        w, v = weights[i], values[i]
        for c in range(capacity, w - 1, -1):
            candidate = dp[c - w] + v
            if candidate > dp[c]:
                dp[c] = candidate
    return dp[capacity]


def knapsack_unbounded(
    weights: Sequence[int], values: Sequence[int], capacity: int
) -> int:
    """Unbounded knapsack: items may be used unlimited times.

    Args:
        weights: Per-item weights.
        values: Per-item values.
        capacity: Maximum total weight.

    Returns:
        Maximum total value achievable.

    Complexity:
        Time: O(n * capacity). Space: O(capacity).
    """
    n = len(weights)
    if n != len(values):
        raise ValueError("weights and values must have the same length")
    dp = [0] * (capacity + 1)
    for c in range(1, capacity + 1):
        for i in range(n):
            w, v = weights[i], values[i]
            if w <= c:
                candidate = dp[c - w] + v
                if candidate > dp[c]:
                    dp[c] = candidate
    return dp[capacity]


def longest_increasing_subsequence(arr: Sequence[int]) -> int:
    """Length of the longest strictly increasing subsequence.

    Args:
        arr: Input sequence of ints.

    Returns:
        Length of the LIS.

    Complexity:
        Time: O(n log n) (patience sorting). Space: O(n).
    """
    if not arr:
        return 0
    tails: list[int] = []
    for x in arr:
        # Binary search for first element >= x
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return len(tails)


def matrix_chain_multiplication(dimensions: Sequence[int]) -> int:
    """Minimum scalar multiplications for matrix chain product.

    ``dimensions`` has length n+1 for n matrices; matrix i has dims
    ``dimensions[i-1] x dimensions[i]``.

    Args:
        dimensions: Chain of matrix dimensions.

    Returns:
        Minimum number of scalar multiplications.

    Complexity:
        Time: O(n^3). Space: O(n^2).
    """
    n = len(dimensions) - 1
    if n < 2:
        return 0
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i - 1] * dimensions[k] * dimensions[j]
                )
                if cost < dp[i][j]:
                    dp[i][j] = cost
    return dp[1][n]


def subset_sum(nums: Sequence[int], target: int) -> bool:
    """Determine whether some subset of ``nums`` sums to ``target``.

    Args:
        nums: Input numbers (assumed non-negative for simplicity).
        target: Target sum.

    Returns:
        True if any subset sums to ``target``, False otherwise.

    Complexity:
        Time: O(n * target). Space: O(target).
    """
    if target < 0:
        return False
    reachable = [False] * (target + 1)
    reachable[0] = True
    for x in nums:
        if x < 0:
            raise ValueError("subset_sum expects non-negative inputs")
        for s in range(target, x - 1, -1):
            if reachable[s - x]:
                reachable[s] = True
    return reachable[target]


def rod_cutting(prices: Sequence[int], n: int) -> int:
    """Maximum revenue from cutting a rod of length ``n``.

    ``prices[i]`` is the sale price of a rod piece of length ``i+1``.

    Args:
        prices: Sale price per piece length 1..len(prices).
        n: Total rod length.

    Returns:
        Maximum revenue.

    Complexity:
        Time: O(n * len(prices)). Space: O(n).
    """
    if n <= 0:
        return 0
    if n > len(prices):
        raise ValueError("n exceeds available piece lengths")
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            candidate = prices[cut - 1] + dp[length - cut]
            if candidate > dp[length]:
                dp[length] = candidate
    return dp[n]


def word_break(s: str, word_dict: Sequence[str]) -> bool:
    """Determine whether ``s`` can be segmented into dictionary words.

    Args:
        s: Input string (non-empty).
        word_dict: Sequence of allowed words.

    Returns:
        True if a valid segmentation exists.

    Complexity:
        Time: O(len(s)^2 * max_word_len). Space: O(len(s)).
    """
    word_set = set(word_dict)
    if not s:
        return True
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(0, i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]


__all__ = [
    "fibonacci_memo",
    "fibonacci_tab",
    "coin_change",
    "longest_common_subsequence",
    "longest_common_substring",
    "edit_distance",
    "knapsack_01",
    "knapsack_unbounded",
    "longest_increasing_subsequence",
    "matrix_chain_multiplication",
    "subset_sum",
    "rod_cutting",
    "word_break",
]