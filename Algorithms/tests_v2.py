"""Tests for the additional modules added in v2.0.

Tests:
    - TestAdvancedGraph (cycle detection, SCC, Johnson, 2-SAT)
    - TestAdvancedTrees (SegmentTree, FenwickTree, SkipList)
    - TestBloomFilter
    - TestSuffixStructures (suffix array, LCP, SAM)
    - TestNetworkFlow (Ford-Fulkerson, min-cut, Hopcroft-Karp)
    - TestAdvancedDP (TSP Held-Karp, LPS, weighted interval, boolean paren, digit DP)
    - TestGeometry (convex hull, 2D closest pair)
    - TestRandomized (reservoir sampling, quickselect, miller-rabin, monte carlo, treap)
"""

from __future__ import annotations

import math
import sys
import unittest

if __name__ in {"__main__", "__mp_main__"} and __package__ in (None, ""):
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Algorithms import (  # noqa: E402
        # advanced graph
        connected_components, has_cycle_directed, has_cycle_undirected,
        johnson, kosaraju_scc, tarjan_scc, two_sat,
        # advanced trees
        FenwickTree, SegmentTree, SkipList,
        # bloom filter
        BloomFilter, CountingBloomFilter,
        # suffix structures
        SuffixAutomaton, build_lcp_array, build_suffix_array,
        suffix_array_search,
        # network flow
        ford_fulkerson, hopcroft_karp, min_cut,
        # advanced dp
        boolean_parenthesization, digit_dp, longest_palindromic_subsequence,
        longest_path_dag, tsp_held_karp, weighted_interval_scheduling,
        # geometry
        closest_pair_2d, convex_hull_graham_scan,
        # randomized
        Treap, fisher_yates_shuffle, miller_rabin, monte_carlo_pi,
        quickselect, reservoir_sample,
    )
else:
    from . import (
        connected_components, has_cycle_directed, has_cycle_undirected,
        johnson, kosaraju_scc, tarjan_scc, two_sat,
        FenwickTree, SegmentTree, SkipList,
        BloomFilter, CountingBloomFilter,
        SuffixAutomaton, build_lcp_array, build_suffix_array,
        suffix_array_search,
        ford_fulkerson, hopcroft_karp, min_cut,
        boolean_parenthesization, digit_dp, longest_palindromic_subsequence,
        longest_path_dag, tsp_held_karp, weighted_interval_scheduling,
        closest_pair_2d, convex_hull_graham_scan,
        Treap, fisher_yates_shuffle, miller_rabin, monte_carlo_pi,
        quickselect, reservoir_sample,
    )


class TestAdvancedGraph(unittest.TestCase):
    def test_has_cycle_undirected_yes(self) -> None:
        # Triangle: a - b - c - a
        self.assertTrue(has_cycle_undirected({"a": ["b", "c"], "b": ["a", "c"], "c": ["b", "a"]}))

    def test_has_cycle_undirected_no(self) -> None:
        # Path: a - b - c
        self.assertFalse(has_cycle_undirected({"a": ["b"], "b": ["a", "c"], "c": ["b"]}))

    def test_has_cycle_directed_yes(self) -> None:
        # 1 -> 2 -> 3 -> 1
        self.assertTrue(has_cycle_directed({"1": ["2"], "2": ["3"], "3": ["1"]}))

    def test_has_cycle_directed_no(self) -> None:
        # DAG
        self.assertFalse(has_cycle_directed({"1": ["2", "3"], "2": ["4"], "3": ["4"], "4": []}))

    def test_connected_components(self) -> None:
        g = {"a": ["b"], "b": ["a"], "c": ["d"], "d": ["c"], "e": []}
        comps = connected_components(g)
        self.assertEqual(len(comps), 3)
        for c in comps:
            if "a" in c:
                self.assertEqual(c, {"a", "b"})

    def test_tarjan_scc(self) -> None:
        g = {"1": ["2"], "2": ["3", "4"], "3": ["1"], "4": ["5"], "5": ["4"]}
        sccs = tarjan_scc(g)
        sets = [set(s) for s in sccs]
        self.assertIn({"1", "2", "3"}, sets)
        self.assertIn({"4", "5"}, sets)

    def test_kosaraju_scc(self) -> None:
        g = {"1": ["2"], "2": ["3", "4"], "3": ["1"], "4": ["5"], "5": ["4"]}
        sccs = kosaraju_scc(g)
        sets = [set(s) for s in sccs]
        self.assertIn({"1", "2", "3"}, sets)
        self.assertIn({"4", "5"}, sets)

    def test_johnson_simple(self) -> None:
        g = {"A": {"B": -1, "C": 4}, "B": {"C": 3, "D": 2}, "C": {}, "D": {"B": 1}}
        nodes = ["A", "B", "C", "D"]
        d = johnson(g, nodes)
        self.assertEqual(d["A"]["C"], 2)  # A->B->C

    def test_two_sat_satisfiable(self) -> None:
        # vars: x0, x1, x2
        # clause (x0 OR x1): (0, 1)
        # clause (!x0 OR x2): (3, 2) — wait, with n_vars=3, n=6 literals:
        #   0=x0, 1=x1, 2=x2, 3=!x0, 4=!x1, 5=!x2
        # So !x0 = 3, x2 = 2. Correct.
        # clause (!x1 OR !x2): (4, 5)
        clauses = [(0, 1), (3, 2), (4, 5)]
        result = two_sat(3, clauses)
        self.assertIsNotNone(result)
        if result is not None:
            self.assertTrue(result[0] or result[1])
            self.assertTrue((not result[0]) or result[2])
            self.assertTrue((not result[1]) or (not result[2]))

    def test_two_sat_unsatisfiable(self) -> None:
        # x0 AND !x0 -> unsatisfiable.
        # With n_vars=2:
        #   0=x0, 1=x1, 2=!x0, 3=!x1
        # clause (x0 OR x0):  (0, 0)
        # clause (!x0 OR !x0): (2, 2)
        clauses = [(0, 0), (2, 2)]
        self.assertIsNone(two_sat(2, clauses))


class TestAdvancedTrees(unittest.TestCase):
    def test_segment_tree_sum(self) -> None:
        st = SegmentTree([1, 3, 5, 7, 9, 11], combine=lambda a, b: a + b, identity=0)
        self.assertEqual(st.query(0, 5), 36)
        self.assertEqual(st.query(1, 3), 15)
        st.update(2, 100)
        self.assertEqual(st.query(0, 5), 131)

    def test_segment_tree_min(self) -> None:
        st = SegmentTree([3, 1, 4, 1, 5, 9, 2, 6], combine=min, identity=float("inf"))
        self.assertEqual(st.query(0, 7), 1)
        self.assertEqual(st.query(2, 5), 1)
        st.update(7, 0)
        self.assertEqual(st.query(0, 7), 0)

    def test_segment_tree_empty(self) -> None:
        st = SegmentTree([], combine=lambda a, b: a + b, identity=0)
        self.assertEqual(st.query(0, 0), 0)
        self.assertEqual(len(st), 0)

    def test_fenwick_tree_basic(self) -> None:
        ft = FenwickTree(values=[1, 3, 5, 7, 9])
        self.assertEqual(ft.query(2), 9)  # 1+3+5
        self.assertEqual(ft.range_query(1, 3), 15)  # 3+5+7
        ft.update(2, 10)  # 5 -> 15
        self.assertEqual(ft.query(2), 19)
        self.assertEqual(ft.range_query(1, 3), 25)

    def test_fenwick_tree_set(self) -> None:
        ft = FenwickTree(values=[1, 2, 3, 4, 5])
        ft.set(2, 100)
        self.assertEqual(ft.range_query(2, 2), 100)
        self.assertEqual(ft.range_query(0, 4), 1 + 2 + 100 + 4 + 5)

    def test_skip_list(self) -> None:
        sl: SkipList[int] = SkipList(seed=42)
        for x in [5, 3, 8, 1, 9, 2]:
            sl.add(x)
        self.assertEqual(len(sl), 6)
        self.assertIn(5, sl)
        self.assertNotIn(7, sl)
        self.assertEqual(sl.to_list(), [1, 2, 3, 5, 8, 9])
        self.assertTrue(sl.discard(5))
        self.assertEqual(sl.to_list(), [1, 2, 3, 8, 9])
        self.assertFalse(sl.discard(5))


class TestBloomFilter(unittest.TestCase):
    def test_no_false_negatives(self) -> None:
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        items = [f"item_{i}" for i in range(500)]
        for x in items:
            bf.add(x)
        for x in items:
            self.assertIn(x, bf)

    def test_bounded_false_positives(self) -> None:
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        for i in range(1000):
            bf.add(f"a_{i}")
        false_positives = sum(1 for i in range(1000) if f"b_{i}" in bf)
        # Allow some headroom; with p=0.01 expected ~10.
        self.assertLess(false_positives, 50)

    def test_counting_bloom_removes(self) -> None:
        cbf = CountingBloomFilter(capacity=100)
        cbf.add("foo")
        cbf.add("foo")
        self.assertIn("foo", cbf)
        cbf.remove("foo")
        self.assertIn("foo", cbf)  # one copy left
        cbf.remove("foo")
        self.assertNotIn("foo", cbf)


class TestSuffixStructures(unittest.TestCase):
    def test_suffix_array_sorted(self) -> None:
        s = "banana"
        sa = build_suffix_array(s)
        suffixes = [s[i:] for i in sa]
        self.assertEqual(suffixes, sorted(suffixes))
        self.assertEqual(set(sa), set(range(len(s))))

    def test_lcp_array(self) -> None:
        s = "banana"
        sa = build_suffix_array(s)
        lcp = build_lcp_array(s, sa)
        # Manual: lcp[0] = 0
        self.assertEqual(lcp[0], 0)
        self.assertEqual(len(lcp), len(s))
        for i in range(1, len(lcp)):
            a, b = sa[i - 1], sa[i]
            expected = len(_lcp_of(s[a:], s[b:]))
            self.assertEqual(lcp[i], expected)

    def test_suffix_array_search(self) -> None:
        s = "mississippi"
        sa = build_suffix_array(s)
        self.assertEqual(suffix_array_search(s, "ssi", sa), [2, 5])
        self.assertEqual(suffix_array_search(s, "zz", sa), [])
        self.assertEqual(suffix_array_search(s, "i", sa), [1, 4, 7, 10])

    def test_suffix_automaton(self) -> None:
        sam = SuffixAutomaton()
        sam.build("banana")
        self.assertIn("ana", sam)
        self.assertIn("ban", sam)
        self.assertIn("banana", sam)
        self.assertNotIn("zebra", sam)
        # banana has 15 distinct substrings (computed manually: 3+4+3+3+1)
        self.assertEqual(sam.count_distinct_substrings(), 15)
        # LCS with "anagram" is "ana" (length 3)
        lcs = sam.longest_common_substring("anagram")
        self.assertEqual(len(lcs), 3)
        self.assertIn(lcs, ("ana", "naa", "aga"))  # any length-3 LCS works
        self.assertIn(lcs[:2], ("an", "na", "ag"))


def _lcp_of(a: str, b: str) -> str:
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return a[:i]
    return a[:n]


class TestNetworkFlow(unittest.TestCase):
    def test_ford_fulkerson_simple(self) -> None:
        # Classic max-flow = 23 (CLRS example simplified)
        g = {
            "s": {"v1": 16, "v2": 13},
            "v1": {"v2": 10, "v3": 12},
            "v2": {"v1": 4, "v4": 14},
            "v3": {"v2": 9, "t": 20},
            "v4": {"v3": 7, "t": 4},
            "t": {},
        }
        self.assertEqual(ford_fulkerson(g, "s", "t"), 23)

    def test_min_cut(self) -> None:
        g = {
            "s": {"a": 3, "b": 1},
            "a": {"t": 3},
            "b": {"t": 5},
            "t": {},
        }
        cut_value, _ = min_cut(g, "s", "t")
        self.assertEqual(cut_value, 4)

    def test_hopcroft_karp(self) -> None:
        g = {"u1": ["v1", "v2"], "u2": ["v1"], "u3": ["v2"]}
        left, right = hopcroft_karp(g, ["u1", "u2", "u3"], ["v1", "v2"])
        self.assertEqual(len(left), 2)  # perfect matching: 2 pairs


class TestAdvancedDP(unittest.TestCase):
    def test_tsp_held_karp(self) -> None:
        # 4 cities in a square; optimal tour = 4.
        dist = [
            [0, 1, 2, 1],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [1, 2, 1, 0],
        ]
        cost, tour = tsp_held_karp(dist, start=0)
        self.assertAlmostEqual(cost, 4.0)
        self.assertEqual(tour[0], 0)
        self.assertEqual(tour[-1], 0)
        self.assertEqual(set(tour), {0, 1, 2, 3})

    def test_lps(self) -> None:
        self.assertEqual(longest_palindromic_subsequence("bbbab"), 4)  # bbbb
        self.assertEqual(longest_palindromic_subsequence("cbbd"), 2)  # bb
        self.assertEqual(longest_palindromic_subsequence(""), 0)

    def test_longest_path_dag(self) -> None:
        # DAG: 0->1(2), 0->2(3), 1->3(4), 2->3(1), 2->4(5), 3->4(1)
        edges = [(0, 1, 2), (0, 2, 3), (1, 3, 4), (2, 3, 1), (2, 4, 5), (3, 4, 1)]
        # Longest path: 0->2->4 = 3+5 = 8
        self.assertEqual(longest_path_dag(5, edges), 8)
        with self.assertRaises(ValueError):
            longest_path_dag(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])

    def test_weighted_interval_scheduling(self) -> None:
        intervals = [
            (1, 3, 5), (2, 5, 6), (4, 7, 8),
            (6, 9, 3), (8, 10, 4), (9, 12, 7),
        ]
        chosen = weighted_interval_scheduling(intervals)
        # Optimal selection: (1,3,5), (4,7,8), (9,12,7) -> weight 20
        self.assertEqual(len(chosen), 3)
        # Verify non-overlap
        chosen_intervals = sorted([intervals[i] for i in chosen], key=lambda x: x[1])
        last_end = -1
        total_weight = 0
        for s, e, w in chosen_intervals:
            self.assertGreaterEqual(s, last_end)
            total_weight += w
            last_end = e
        self.assertEqual(total_weight, 20)

    def test_boolean_parenthesization(self) -> None:
        # T | F ^ T  -> 1 way to True: T | (F^T) = T|T = T.
        # (T|F) ^T = T^T = F. So only 1.
        self.assertEqual(boolean_parenthesization([True, False, True], ["|", "^"]), 1)
        # F ^ F ^ F  -> 0 ways (XOR of three Fs is F)
        self.assertEqual(boolean_parenthesization([False, False, False], ["^", "^"]), 0)

    def test_digit_dp(self) -> None:
        # Count integers in [0, 100] without digit '9'.
        # 0-9: 9 (skip 9), 10-19: 9, ..., 90-99: 9, 100: 1 = 82.
        count = digit_dp(100, lambda d: 9 not in d)
        self.assertEqual(count, 82)


class TestGeometry(unittest.TestCase):
    def test_convex_hull(self) -> None:
        pts = [(0, 0), (1, 1), (2, 0), (2, 2), (0, 2), (1, 0.5)]
        hull = convex_hull_graham_scan(pts)
        hull_set = set(hull)
        self.assertIn((0, 0), hull_set)
        self.assertIn((2, 0), hull_set)
        self.assertIn((2, 2), hull_set)
        self.assertIn((0, 2), hull_set)
        # (1, 0.5) is interior, should NOT be in hull
        self.assertNotIn((1, 0.5), hull_set)

    def test_convex_hull_collinear(self) -> None:
        pts = [(0, 0), (1, 0), (2, 0), (3, 0)]
        hull = convex_hull_graham_scan(pts)
        # Only the two endpoints of the line remain
        self.assertEqual(len(hull), 2)

    def test_closest_pair_2d(self) -> None:
        pts = [(0, 0), (1, 0), (5, 0), (8, 0), (0, 1)]
        self.assertAlmostEqual(closest_pair_2d(pts), 1.0)
        self.assertEqual(closest_pair_2d([(0, 0)]), float("inf"))


class TestRandomized(unittest.TestCase):
    def test_reservoir_sample_count(self) -> None:
        sample = reservoir_sample(range(100), k=10, seed=0)
        self.assertEqual(len(sample), 10)
        self.assertEqual(len(set(sample)), 10)
        self.assertTrue(all(0 <= x < 100 for x in sample))

    def test_fisher_yates(self) -> None:
        original = list(range(20))
        shuffled = fisher_yates_shuffle(original, seed=42)
        self.assertEqual(sorted(shuffled), original)
        self.assertNotEqual(shuffled, original)  # with seed=42 should differ

    def test_quickselect(self) -> None:
        arr = [7, 4, 1, 9, 3, 8, 2, 6, 5]
        for k in range(len(arr)):
            result = quickselect(arr, k, seed=42)
            expected = sorted(arr)[k]
            self.assertEqual(result, expected)

    def test_miller_rabin(self) -> None:
        # Known primes
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 97, 101, 7919]:
            self.assertTrue(miller_rabin(p), f"{p} should be prime")
        # Known composites
        for c in [4, 6, 8, 9, 15, 21, 25, 27, 35, 49]:
            self.assertFalse(miller_rabin(c), f"{c} should be composite")

    def test_miller_rabin_invalid(self) -> None:
        with self.assertRaises(ValueError):
            miller_rabin(1)
        with self.assertRaises(ValueError):
            miller_rabin(0)

    def test_monte_carlo_pi(self) -> None:
        pi_est = monte_carlo_pi(samples=100_000, seed=0)
        # Should be within ~0.05 of true pi with this many samples.
        self.assertLess(abs(pi_est - math.pi), 0.05)

    def test_treap_basic(self) -> None:
        t: Treap[str] = Treap(seed=42)
        t.insert(5, "five")
        t.insert(2, "two")
        t.insert(8, "eight")
        t.insert(3, "three")
        self.assertEqual(t.search(3), "three")
        self.assertIsNone(t.search(99))
        self.assertIn(2, t)
        t.delete(2)
        self.assertNotIn(2, t)


if __name__ == "__main__":
    unittest.main()