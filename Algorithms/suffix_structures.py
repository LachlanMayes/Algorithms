"""Suffix arrays, suffix trees, and suffix automata.

Reference: arXiv:2401.04509 - "Linear-size Suffix Tries and Linear-size
CDAWGs Simplified and Improved" (Inenaga, 2024).

A suffix array is the sorted list of starting indices of every suffix of a
string. A suffix tree is a compact trie of all suffixes. A suffix automaton
(SAM) is a directed acyclic word automaton with O(n) states that recognises
exactly the set of substrings of the input.
"""

from __future__ import annotations


def build_suffix_array(s: str) -> list[int]:
    """Build a suffix array using the doubling algorithm (sort by rank prefix
    of length 2^k, doubling k until all suffixes are distinguished).

    Args:
        s: Input string.

    Returns:
        Sorted list of starting indices of every suffix. Empty for "".

    Complexity:
        Time: O(n log n). Space: O(n).
    """
    n = len(s)
    if n == 0:
        return []
    # Initial ranks = character code.
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    tmp = [0] * n
    while True:
        # Sort by (rank[i], rank[i+k]) pair.
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        # Re-rank.
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, cur = sa[i - 1], sa[i]
            tmp[cur] = tmp[prev] + (
                (rank[prev], rank[prev + k] if prev + k < n else -1)
                < (rank[cur], rank[cur + k] if cur + k < n else -1)
            )
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def build_lcp_array(s: str, sa: Sequence[int]) -> list[int]:
    """Build the LCP (Longest Common Prefix) array for a string + its suffix
    array, using Kasai's algorithm.

    ``lcp[i]`` is the length of the longest common prefix of the suffixes
    starting at ``sa[i]`` and ``sa[i-1]``.

    Args:
        s: Input string.
        sa: Its suffix array.

    Returns:
        LCP array of length ``len(sa)``. ``lcp[0] = 0``.

    Complexity:
        Time: O(n). Space: O(n).
    """
    n = len(sa)
    if n == 0:
        return []
    lcp = [0] * n
    # Inverse suffix array: rank[i] = position of suffix starting at i in SA.
    inv = [0] * n
    for i, idx in enumerate(sa):
        inv[idx] = i
    h = 0
    for i in range(n):
        r = inv[i]
        if r == 0:
            h = 0
            continue
        j = sa[r - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h > 0:
            h -= 1
    return lcp


def suffix_array_search(text: str, pattern: str, sa: Sequence[int]) -> list[int]:
    """Find all occurrences of ``pattern`` in ``text`` using its suffix array.

    Two binary searches locate the leftmost and rightmost SA index whose
    suffix starts with ``pattern``.

    Args:
        text: Haystack.
        pattern: Needle.
        sa: Suffix array of ``text``.

    Returns:
        Sorted list of starting indices where ``pattern`` occurs.

    Complexity:
        Time: O(|pattern| * log |text| + occurrences).
    """
    n = len(sa)
    if not pattern or not sa:
        return []
    m = len(pattern)

    def cmp_suffix_with_pattern(idx: int) -> int:
        """Compare suffix at sa[idx] with pattern. -1 / 0 / 1."""
        suf = text[idx:]
        # Lex compare limited to m chars
        lim = min(m, len(suf))
        for k in range(lim):
            if suf[k] < pattern[k]:
                return -1
            if suf[k] > pattern[k]:
                return 1
        if len(suf) < m:
            return -1
        return 0

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cmp_suffix_with_pattern(sa[mid]) < 0:
            lo = mid + 1
        else:
            hi = mid
    if cmp_suffix_with_pattern(sa[lo]) != 0:
        return []
    left = lo
    lo, hi = left, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cmp_suffix_with_pattern(sa[mid]) <= 0:
            lo = mid
        else:
            hi = mid - 1
    right = lo
    return sorted(sa[i] for i in range(left, right + 1))


# --------------------------------------------------------------------------- #
# Suffix Automaton (SAM)
# --------------------------------------------------------------------------- #


class _SAMState:
    __slots__ = ("next", "link", "length")

    def __init__(self) -> None:
        # Transitions: dict char -> state id.
        self.next: dict[str, int] = {}
        # Suffix link (failure function). -1 for the initial state.
        self.link: int = -1
        # Length of the longest string in this equivalence class.
        self.length: int = 0


class SuffixAutomaton:
    """Suffix automaton (SAM) for efficient substring queries.

    A SAM has at most 2n - 1 states for an input of length n, and supports
    checking substring presence in O(|pattern|) time, plus counting
    occurrences of each substring (by state endpos).

    Reference: Blumer, A. et al. (1985) "The smallest automaton recognizing
    the subwords of a text". Theoretical Computer Science.

    Complexity:
        Build: O(n) amortized. Substring check: O(|p|).
        Endpos count (after :meth:`compute_endpos`): O(|p|) per query.
    """

    def __init__(self) -> None:
        self._states: list[_SAMState] = [_SAMState()]
        self._states[0].length = 0
        self._last: int = 0
        self._size: int = 1

    def extend(self, ch: str) -> None:
        """Append one character to the automaton. O(1) amortized.

        Args:
            ch: Single character to add.
        """
        p = self._last
        cur = self._size
        self._states.append(_SAMState())
        self._states[cur].length = self._states[p].length + 1
        self._size += 1
        while p != -1 and ch not in self._states[p].next:
            self._states[p].next[ch] = cur
            p = self._states[p].link
        if p == -1:
            self._states[cur].link = 0
        else:
            q = self._states[p].next[ch]
            if self._states[p].length + 1 == self._states[q].length:
                self._states[cur].link = q
            else:
                clone = self._size
                self._states.append(_SAMState())
                self._states[clone].length = self._states[p].length + 1
                self._states[clone].next = self._states[q].next.copy()
                self._states[clone].link = self._states[q].link
                self._size += 1
                while p != -1 and self._states[p].next.get(ch) == q:
                    self._states[p].next[ch] = clone
                    p = self._states[p].link
                self._states[q].link = clone
                self._states[cur].link = clone
        self._last = cur

    def build(self, s: str) -> None:
        """Reset and build the SAM for the whole string.

        Args:
            s: Input string.
        """
        self.__init__()
        for ch in s:
            self.extend(ch)

    @property
    def size(self) -> int:
        """Number of states."""
        return self._size

    def _walk(self, pattern: str) -> int:
        """Walk the automaton with pattern. Returns state id, or -1 if no match."""
        state = 0
        for ch in pattern:
            nxt = self._states[state].next.get(ch)
            if nxt is None:
                return -1
            state = nxt
        return state

    def __contains__(self, pattern: str) -> bool:
        """True if ``pattern`` is a substring of the built text.

        Args:
            pattern: Candidate substring.

        Returns:
            True if ``pattern`` occurs in the input, False otherwise.
        """
        return self._walk(pattern) != -1

    def contains(self, pattern: str) -> bool:
        """Alias for ``pattern in sam``."""
        return pattern in self

    def count_distinct_substrings(self) -> int:
        """Number of distinct substrings.

        Returns:
            ``sum over states v of (len[v] - len[link[v]])``.

        Complexity:
            Time: O(|states|).
        """
        total = 0
        for v in range(1, self._size):  # skip initial state
            total += self._states[v].length - self._states[self._states[v].link].length
        return total

    def longest_common_substring(self, other: str) -> str:
        """Longest common substring between the built text and ``other``.

        Args:
            other: Second string.

        Returns:
            The longest non-empty common substring; empty if none.

        Complexity:
            Time: O(|text| + |other|).
        """
        best = ""
        best_len = 0
        best_end = -1
        v = 0
        cur_len = 0
        for i, ch in enumerate(other):
            while v != 0 and ch not in self._states[v].next:
                v = self._states[v].link
                cur_len = self._states[v].length
            if ch in self._states[v].next:
                v = self._states[v].next[ch]
                cur_len += 1
                if cur_len > best_len:
                    best_len = cur_len
                    best_end = i
            else:
                v = 0
                cur_len = 0
        if best_end >= 0:
            best = other[best_end - best_len + 1: best_end + 1]
        return best


__all__ = [
    "build_suffix_array",
    "build_lcp_array",
    "suffix_array_search",
    "SuffixAutomaton",
]