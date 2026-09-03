"""String algorithms.

Implementations of classic string-matching, palindrome-finding, and
encoding utilities.
"""

from __future__ import annotations

from collections import Counter


def rabin_karp(text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7) -> list[int]:
    """Rabin-Karp substring search using rolling hash.

    Args:
        text: Haystack string.
        pattern: Needle string.
        base: Rolling hash base (e.g. number of characters in alphabet).
        mod: Hash modulus.

    Returns:
        Starting indices where ``pattern`` occurs in ``text``.

    Complexity:
        Time: O(n + m) average, O(n*m) worst case with collisions.
        Space: O(1) extra (excluding output).
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    p_hash = 0
    t_hash = 0
    power = 1
    for i in range(m - 1):
        power = (power * base) % mod
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    out: list[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                out.append(i)
        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * power) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
            if t_hash < 0:
                t_hash += mod
    return out


def kmp_search(text: str, pattern: str) -> list[int]:
    """Knuth-Morris-Pratt substring search.

    Args:
        text: Haystack.
        pattern: Needle.

    Returns:
        Starting indices where ``pattern`` occurs in ``text``.

    Complexity:
        Time: O(n + m). Space: O(m).
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    # Build the longest-proper-prefix-which-is-also-suffix (failure) table
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = fail[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        fail[i] = k

    out: list[int] = []
    k = 0
    for i in range(n):
        while k > 0 and pattern[k] != text[i]:
            k = fail[k - 1]
        if pattern[k] == text[i]:
            k += 1
        if k == m:
            out.append(i - m + 1)
            k = fail[k - 1]
    return out


def naive_string_match(text: str, pattern: str) -> list[int]:
    """Brute-force substring search.

    Args:
        text: Haystack.
        pattern: Needle.

    Returns:
        Starting indices where ``pattern`` occurs in ``text``.

    Complexity:
        Time: O(n * m). Space: O(1).
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    out: list[int] = []
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            out.append(i)
    return out


def z_algorithm(s: str) -> list[int]:
    """Z-algorithm: compute Z-array where ``Z[i]`` is the length of the longest
    substring starting at i that is also a prefix of s.

    Args:
        s: Input string.

    Returns:
        List of ints of length ``len(s)``. Z[0] is conventionally 0.

    Complexity:
        Time: O(n). Space: O(n).
    """
    n = len(s)
    z = [0] * n
    if n == 0:
        return z
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def longest_palindromic_substring(s: str) -> str:
    """Longest contiguous palindromic substring (expand-around-centers).

    Args:
        s: Input string.

    Returns:
        The longest palindromic substring. Empty string if ``s`` is empty.

    Complexity:
        Time: O(n^2). Space: O(1).
    """
    if not s:
        return ""
    start, end = 0, 0
    for i in range(len(s)):
        len1 = _expand(s, i, i)
        len2 = _expand(s, i, i + 1)
        length = max(len1, len2)
        if length > end - start + 1:
            start = i - (length - 1) // 2
            end = i + length // 2
    return s[start:end + 1]


def _expand(s: str, left: int, right: int) -> int:
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1


def manacher_palindromes(s: str) -> str:
    """Longest palindromic substring via Manacher's algorithm.

    Args:
        s: Input string.

    Returns:
        Longest palindromic substring.

    Complexity:
        Time: O(n). Space: O(n).
    """
    if not s:
        return ""
    t = "#" + "#".join(s) + "#"
    n = len(t)
    p = [0] * n
    c = r = 0
    for i in range(n):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])
        while (
            i + p[i] + 1 < n
            and i - p[i] - 1 >= 0
            and t[i + p[i] + 1] == t[i - p[i] - 1]
        ):
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    length, center = max((p[i], i) for i in range(n))
    start = (center - length) // 2
    return s[start:start + length]


def anagram_check(s1: str, s2: str) -> bool:
    """Two strings are anagrams of each other (whitespace-insensitive).

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        True if they are anagrams, False otherwise.

    Complexity:
        Time: O(n). Space: O(k) where k is the alphabet size.
    """
    c1 = Counter(s1.replace(" ", "").lower())
    c2 = Counter(s2.replace(" ", "").lower())
    return c1 == c2


def run_length_encoding(s: str) -> str:
    """Run-length encode a string (counts of consecutive identical chars).

    Args:
        s: Input string.

    Returns:
        Encoded form, e.g. ``"aaabbc" -> "3a2b1c"``. Empty input -> ``""``.

    Complexity:
        Time: O(n). Space: O(n).
    """
    if not s:
        return ""
    out: list[str] = []
    prev = s[0]
    count = 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append(f"{count}{prev}")
            prev = ch
            count = 1
    out.append(f"{count}{prev}")
    return "".join(out)


__all__ = [
    "rabin_karp",
    "kmp_search",
    "naive_string_match",
    "z_algorithm",
    "longest_palindromic_substring",
    "manacher_palindromes",
    "anagram_check",
    "run_length_encoding",
]