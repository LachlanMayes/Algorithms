"""Comprehensive unit tests for the Algorithms library.

Run with (from the parent directory)::

    python -m unittest Algorithms.tests -v

or (from inside the ``Algorithms/`` subdirectory)::

    python tests.py

All tests are pure-stdlib and have no external dependencies.
"""

from __future__ import annotations

import sys
import unittest

# Allow running this file directly (``python tests.py``) without the package
# being on sys.path. We do this by ensuring the package's parent dir is
# importable so ``import Algorithms`` works.
if __name__ in {"__main__", "__mp_main__"} and __package__ in (None, ""):
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Algorithms import (  # noqa: E402
        # searching
        binary_search, binary_search_recursive, exponential_search,
        interpolation_search, jump_search, linear_search, ternary_search,
        # sorting
        bubble_sort, counting_sort, heap_sort, insertion_sort, merge_sort,
        quicksort, radix_sort, selection_sort, shell_sort,
        # graph
        a_star, bellman_ford, bfs, dfs, dfs_recursive, dijkstra,
        floyd_warshall, kruskal_mst, prim_mst, topological_sort,
        # data structures
        BinarySearchTree, DoublyLinkedList, Graph, LRUCache, LinkedList,
        MaxHeap, MinHeap, Queue, Stack, Trie, UnionFind,
        # dynamic programming
        coin_change, edit_distance, fibonacci_memo, fibonacci_tab,
        knapsack_01, knapsack_unbounded, longest_common_substring,
        longest_common_subsequence, longest_increasing_subsequence,
        matrix_chain_multiplication, rod_cutting, subset_sum, word_break,
        # greedy
        activity_selection, fractional_knapsack, gas_station_circuit,
        huffman_coding, job_sequencing, minimum_coins,
        # divide & conquer
        closest_pair, count_inversions, find_max, find_max_min, karatsuba,
        merge_sort as merge_sort_dc, power, quicksort as quicksort_dc,
        quicksort_inplace, strassen_matrix_multiply,
        # string algorithms
        anagram_check, kmp_search, longest_palindromic_substring,
        manacher_palindromes, naive_string_match, rabin_karp,
        run_length_encoding, z_algorithm,
        # number theory
        euler_totient, factorial, fibonacci, gcd, is_prime, lcm,
        modular_exponentiation, prime_factorization,
        sieve_of_eratosthenes,
    )
else:
    from . import (
        binary_search, binary_search_recursive, exponential_search,
        interpolation_search, jump_search, linear_search, ternary_search,
        bubble_sort, counting_sort, heap_sort, insertion_sort, merge_sort,
        quicksort, radix_sort, selection_sort, shell_sort,
        a_star, bellman_ford, bfs, dfs, dfs_recursive, dijkstra,
        floyd_warshall, kruskal_mst, prim_mst, topological_sort,
        BinarySearchTree, DoublyLinkedList, Graph, LRUCache, LinkedList,
        MaxHeap, MinHeap, Queue, Stack, Trie, UnionFind,
        coin_change, edit_distance, fibonacci_memo, fibonacci_tab,
        knapsack_01, knapsack_unbounded, longest_common_substring,
        longest_common_subsequence, longest_increasing_subsequence,
        matrix_chain_multiplication, rod_cutting, subset_sum, word_break,
        activity_selection, fractional_knapsack, gas_station_circuit,
        huffman_coding, job_sequencing, minimum_coins,
        closest_pair, count_inversions, find_max, find_max_min, karatsuba,
        merge_sort as merge_sort_dc, power, quicksort as quicksort_dc,
        quicksort_inplace, strassen_matrix_multiply,
        anagram_check, kmp_search, longest_palindromic_substring,
        manacher_palindromes, naive_string_match, rabin_karp,
        run_length_encoding, z_algorithm,
        euler_totient, factorial, fibonacci, gcd, is_prime, lcm,
        modular_exponentiation, prime_factorization,
        sieve_of_eratosthenes,
    )


# --------------------------------------------------------------------------- #
# Searching
# --------------------------------------------------------------------------- #


class TestSearching(unittest.TestCase):
    def test_linear_search(self) -> None:
        self.assertEqual(linear_search([5, 3, 8, 1], 8), 2)
        self.assertEqual(linear_search([], 1), -1)
        self.assertEqual(linear_search([1], 1), 0)
        self.assertEqual(linear_search([1, 2, 3], 4), -1)
        self.assertEqual(linear_search(["a", "b", "c"], "b"), 1)

    def test_binary_search(self) -> None:
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 5), 2)
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 1), 0)
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 9), 4)
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 4), -1)
        self.assertEqual(binary_search([], 1), -1)
        self.assertEqual(binary_search([1], 1), 0)

    def test_binary_search_recursive(self) -> None:
        arr = [2, 4, 6, 8, 10]
        self.assertEqual(binary_search_recursive(arr, 6), 2)
        self.assertEqual(binary_search_recursive(arr, 11), -1)

    def test_ternary_search(self) -> None:
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i, v in enumerate(arr):
            self.assertEqual(ternary_search(arr, v), i)
        self.assertEqual(ternary_search(arr, 10), -1)

    def test_jump_search(self) -> None:
        arr = [10, 20, 30, 40, 50, 60, 70]
        self.assertEqual(jump_search(arr, 40), 3)
        self.assertEqual(jump_search(arr, 11), -1)
        self.assertEqual(jump_search([], 1), -1)

    def test_interpolation_search(self) -> None:
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        self.assertEqual(interpolation_search(arr, 70), 6)
        self.assertEqual(interpolation_search(arr, 5), -1)
        self.assertEqual(interpolation_search(arr, 95), -1)

    def test_exponential_search(self) -> None:
        arr = [2, 4, 6, 8, 10, 12, 14, 16]
        self.assertEqual(exponential_search(arr, 8), 3)
        self.assertEqual(exponential_search(arr, 16), 7)
        self.assertEqual(exponential_search(arr, 1), -1)


# --------------------------------------------------------------------------- #
# Sorting
# --------------------------------------------------------------------------- #


class TestSorting(unittest.TestCase):
    def test_bubble(self) -> None:
        self.assertEqual(bubble_sort([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])
        self.assertEqual(bubble_sort([]), [])
        self.assertEqual(bubble_sort([1]), [1])
        self.assertEqual(bubble_sort([2, 2, 2]), [2, 2, 2])

    def test_selection(self) -> None:
        self.assertEqual(selection_sort([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])
        self.assertEqual(selection_sort([3, 3, 1]), [1, 3, 3])

    def test_insertion(self) -> None:
        self.assertEqual(insertion_sort([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])
        self.assertEqual(insertion_sort([1, 2, 3]), [1, 2, 3])

    def test_merge(self) -> None:
        self.assertEqual(merge_sort([5, 3, 1, 4, 2, 8, 6]), [1, 2, 3, 4, 5, 6, 8])
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([1]), [1])

    def test_quicksort(self) -> None:
        self.assertEqual(quicksort([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])
        self.assertEqual(quicksort([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(quicksort([3, 3, 3]), [3, 3, 3])

    def test_heap(self) -> None:
        arr = [5, 3, 1, 4, 2]
        self.assertEqual(heap_sort(arr), [1, 2, 3, 4, 5])

    def test_shell(self) -> None:
        self.assertEqual(shell_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]), list(range(1, 10)))

    def test_counting(self) -> None:
        self.assertEqual(counting_sort([4, 2, 2, 8, 3, 3, 1]), [1, 2, 2, 3, 3, 4, 8])
        self.assertEqual(counting_sort([]), [])
        with self.assertRaises(ValueError):
            counting_sort([-1, 2, 3])

    def test_radix(self) -> None:
        self.assertEqual(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]),
                         [2, 24, 45, 66, 75, 90, 170, 802])

    def test_sort_correctness_large(self) -> None:
        import random
        data = [random.randint(-1000, 1000) for _ in range(500)]
        self.assertEqual(quicksort(data), sorted(data))
        self.assertEqual(merge_sort(data), sorted(data))


# --------------------------------------------------------------------------- #
# Graph Algorithms
# --------------------------------------------------------------------------- #


class TestGraphAlgorithms(unittest.TestCase):
    def setUp(self) -> None:
        self.g = {
            "A": {"B": 1, "C": 4},
            "B": {"A": 1, "C": 2, "D": 5},
            "C": {"A": 4, "B": 2, "D": 1},
            "D": {"B": 5, "C": 1},
        }

    def test_bfs(self) -> None:
        order = bfs(self.g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})

    def test_dfs(self) -> None:
        order = dfs(self.g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})

    def test_dfs_recursive(self) -> None:
        order = dfs_recursive(self.g, "A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})

    def test_dijkstra(self) -> None:
        d = dijkstra(self.g, "A")
        self.assertEqual(d["A"], 0)
        self.assertEqual(d["D"], 4)  # A->B->C->D = 1+2+1

    def test_dijkstra_negative_weight(self) -> None:
        with self.assertRaises(ValueError):
            dijkstra({"A": {"B": -1}}, "A")

    def test_bellman_ford(self) -> None:
        g = {"A": {"B": 4, "C": 5}, "B": {"C": -3}, "C": {}}
        d = bellman_ford(g, "A")
        self.assertEqual(d["A"], 0)
        self.assertEqual(d["B"], 4)
        self.assertEqual(d["C"], 1)

    def test_bellman_ford_negative_cycle(self) -> None:
        g = {"A": {"B": 1}, "B": {"C": -3}, "C": {"A": 1}}
        with self.assertRaises(ValueError):
            bellman_ford(g, "A")

    def test_floyd_warshall(self) -> None:
        d = floyd_warshall(self.g)
        self.assertEqual(d["A"]["A"], 0)
        self.assertEqual(d["A"]["D"], 4)

    def test_topological_sort(self) -> None:
        g = {
            "A": {"B": 1, "C": 1},
            "B": {"D": 1},
            "C": {"D": 1},
            "D": {},
        }
        order = topological_sort(g)
        self.assertEqual(order[0], "A")
        self.assertEqual(order[-1], "D")
        self.assertLess(order.index("A"), order.index("D"))

    def test_topological_sort_cycle(self) -> None:
        with self.assertRaises(ValueError):
            topological_sort({"A": {"B": 1}, "B": {"A": 1}})

    def test_kruskal_mst(self) -> None:
        edges = [
            ("A", "B", 1), ("A", "C", 3), ("B", "C", 1),
            ("B", "D", 4), ("C", "D", 1),
        ]
        mst = kruskal_mst(4, edges)
        self.assertEqual(len(mst), 3)
        self.assertEqual(sum(w for _, _, w in mst), 3)

    def test_prim_mst(self) -> None:
        ug = {
            "A": {"B": 1, "C": 3},
            "B": {"A": 1, "C": 1, "D": 4},
            "C": {"A": 3, "B": 1, "D": 1},
            "D": {"B": 4, "C": 1},
        }
        mst = prim_mst(ug, "A")
        self.assertEqual(len(mst), 3)
        self.assertEqual(sum(w for _, _, w in mst), 3)

    def test_a_star(self) -> None:
        g = {
            "A": {"B": 1, "C": 1},
            "B": {"D": 1},
            "C": {"D": 1},
            "D": {},
        }
        path = a_star(g, "A", "D", lambda _: 0)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "D")
        self.assertEqual(len(path), 3)

    def test_a_star_no_path(self) -> None:
        g = {"A": {"B": 1}, "C": {}}
        self.assertEqual(a_star(g, "A", "C", lambda _: 0), [])


# --------------------------------------------------------------------------- #
# Data Structures
# --------------------------------------------------------------------------- #


class TestDataStructures(unittest.TestCase):
    def test_stack(self) -> None:
        s: Stack[int] = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        s.push(2)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.size(), 1)
        with self.assertRaises(IndexError):
            Stack().pop()

    def test_queue(self) -> None:
        q: Queue[int] = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.size(), 2)

    def test_linked_list(self) -> None:
        ll: LinkedList[int] = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.prepend(0)
        self.assertEqual(ll.display(), [0, 1, 2])
        self.assertEqual(ll.find(1), 1)
        self.assertTrue(ll.delete(1))
        self.assertEqual(ll.display(), [0, 2])

    def test_doubly_linked_list(self) -> None:
        dll: DoublyLinkedList[int] = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        dll.prepend(0)
        self.assertEqual(dll.display(), [0, 1, 2])
        self.assertTrue(dll.delete(1))
        self.assertEqual(dll.display(), [0, 2])

    def test_bst(self) -> None:
        bst: BinarySearchTree[int] = BinarySearchTree()
        for v in [5, 3, 7, 1, 4, 6, 8]:
            bst.insert(v)
        self.assertEqual(bst.inorder(), [1, 3, 4, 5, 6, 7, 8])
        self.assertTrue(bst.search(4))
        self.assertFalse(bst.search(99))
        bst.delete(3)
        self.assertNotIn(3, bst.inorder())
        bst.delete(5)
        self.assertNotIn(5, bst.inorder())

    def test_trie(self) -> None:
        t = Trie()
        for w in ["apple", "app", "apricot", "banana"]:
            t.insert(w)
        self.assertTrue(t.search("app"))
        self.assertFalse(t.search("appl"))
        self.assertTrue(t.starts_with("apr"))
        self.assertFalse(t.starts_with("zoo"))

    def test_min_heap(self) -> None:
        h: MinHeap[int] = MinHeap([5, 3, 8, 1, 9, 2])
        self.assertEqual(h.peek(), 1)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        h.push(0)
        self.assertEqual(h.pop(), 0)

    def test_max_heap(self) -> None:
        h: MaxHeap[int] = MaxHeap([3, 5, 1, 4, 2])
        self.assertEqual(h.peek(), 5)
        self.assertEqual(h.pop(), 5)

    def test_heap_from_empty(self) -> None:
        self.assertEqual(MinHeap().size(), 0)
        with self.assertRaises(IndexError):
            MinHeap().pop()

    def test_union_find(self) -> None:
        uf: UnionFind[int] = UnionFind(range(5))
        uf.union(0, 1)
        uf.union(2, 3)
        self.assertTrue(uf.connected(0, 1))
        self.assertTrue(uf.connected(2, 3))
        self.assertFalse(uf.connected(0, 2))
        uf.union(1, 3)
        self.assertTrue(uf.connected(0, 2))

    def test_graph(self) -> None:
        g = Graph[str]()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        order = g.bfs("A")
        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C"})

    def test_lru_cache(self) -> None:
        c: LRUCache[int, str] = LRUCache(2)
        c.put(1, "a")
        c.put(2, "b")
        self.assertEqual(c.get(1), "a")
        c.put(3, "c")
        with self.assertRaises(KeyError):
            c.get(2)


# --------------------------------------------------------------------------- #
# Dynamic Programming
# --------------------------------------------------------------------------- #


class TestDynamicProgramming(unittest.TestCase):
    def test_fibonacci_memo(self) -> None:
        for n, expected in [(0, 0), (1, 1), (10, 55), (20, 6765)]:
            self.assertEqual(fibonacci_memo(n), expected)

    def test_fibonacci_tab(self) -> None:
        for n, expected in [(0, 0), (1, 1), (10, 55), (20, 6765)]:
            self.assertEqual(fibonacci_tab(n), expected)

    def test_coin_change(self) -> None:
        self.assertEqual(coin_change([1, 5, 10, 25], 41), 4)
        self.assertEqual(coin_change([2], 3), -1)
        self.assertEqual(coin_change([1], 0), 0)

    def test_lcs(self) -> None:
        self.assertEqual(longest_common_subsequence("abcde", "ace"), 3)
        self.assertEqual(longest_common_subsequence("abc", "abc"), 3)
        self.assertEqual(longest_common_subsequence("", "abc"), 0)

    def test_lcsubstring(self) -> None:
        self.assertEqual(longest_common_substring("abcde", "abfde"), 2)
        self.assertEqual(longest_common_substring("aaaa", "aa"), 2)

    def test_edit_distance(self) -> None:
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("abc", "abc"), 0)

    def test_knapsack_01(self) -> None:
        self.assertEqual(knapsack_01([2, 3, 4, 5], [3, 4, 5, 6], 5), 7)

    def test_knapsack_unbounded(self) -> None:
        self.assertEqual(knapsack_unbounded([1, 3, 4], [15, 20, 30], 4), 60)

    def test_lis(self) -> None:
        self.assertEqual(longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(longest_increasing_subsequence([]), 0)
        self.assertEqual(longest_increasing_subsequence([5, 4, 3, 2, 1]), 1)

    def test_matrix_chain(self) -> None:
        # Classic CLRS example with dims [30,35,15,5,10,20,25] -> 15125.
        self.assertEqual(
            matrix_chain_multiplication([30, 35, 15, 5, 10, 20, 25]), 15125
        )
        # Single matrix -> 0 multiplications.
        self.assertEqual(matrix_chain_multiplication([5, 10]), 0)
        # Two matrices: cost = a*b*c.
        self.assertEqual(matrix_chain_multiplication([2, 3, 4]), 24)

    def test_subset_sum(self) -> None:
        self.assertTrue(subset_sum([3, 34, 4, 12, 5, 2], 9))
        self.assertFalse(subset_sum([3, 34, 4, 12, 5, 2], 30))

    def test_rod_cutting(self) -> None:
        prices = [1, 5, 8, 9, 10, 17, 17, 20]
        self.assertEqual(rod_cutting(prices, 4), 10)

    def test_word_break(self) -> None:
        self.assertTrue(word_break("leetcode", ["leet", "code"]))
        self.assertFalse(word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))


# --------------------------------------------------------------------------- #
# Greedy
# --------------------------------------------------------------------------- #


class TestGreedy(unittest.TestCase):
    def test_activity_selection(self) -> None:
        start = [1, 3, 0, 5, 8, 5]
        end = [2, 4, 6, 7, 9, 9]
        chosen = activity_selection(start, end)
        # Maximum: pick (1,2), (3,4), (5,7), (8,9) -> 4 activities.
        self.assertEqual(len(chosen), 4)
        # The chosen set must be non-overlapping.
        chosen.sort(key=lambda i: end[i])
        for prev, curr in zip(chosen, chosen[1:]):
            self.assertGreaterEqual(start[curr], end[prev])

    def test_fractional_knapsack(self) -> None:
        v = fractional_knapsack([10, 20, 30], [60, 100, 120], 50)
        self.assertAlmostEqual(v, 240.0, places=5)

    def test_huffman_coding(self) -> None:
        # 4-symbol example.
        codes = huffman_coding(["a", "b", "c", "d"], [5, 9, 12, 13])
        self.assertEqual(set(codes.keys()), {"a", "b", "c", "d"})
        # All codes are non-empty.
        for v in codes.values():
            self.assertGreater(len(v), 0)
        # No code is a prefix of another (prefix-free).
        rev = sorted(codes.values(), key=len)
        for i, c in enumerate(rev):
            for other in rev[i + 1:]:
                self.assertFalse(other.startswith(c))

    def test_huffman_coding_single(self) -> None:
        self.assertEqual(huffman_coding(["x"], [5]), {"x": "0"})
        self.assertEqual(huffman_coding([], []), {})

    def test_job_sequencing(self) -> None:
        jobs = ["j1", "j2", "j3", "j4"]
        deadlines = [4, 1, 1, 1]
        profits = [20, 10, 40, 30]
        scheduled = job_sequencing(jobs, deadlines, profits)
        self.assertEqual(len(scheduled), 2)

    def test_minimum_coins(self) -> None:
        self.assertEqual(minimum_coins([1, 5, 10, 25], 41), 4)
        self.assertEqual(minimum_coins([1, 5, 10, 25], 0), 0)
        self.assertEqual(minimum_coins([2], 3), -1)

    def test_gas_station_circuit(self) -> None:
        self.assertEqual(gas_station_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3)
        self.assertEqual(gas_station_circuit([2, 3, 4], [3, 4, 3]), -1)


# --------------------------------------------------------------------------- #
# Divide & Conquer
# --------------------------------------------------------------------------- #


class TestDivideAndConquer(unittest.TestCase):
    def test_merge_sort(self) -> None:
        self.assertEqual(merge_sort_dc([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])
        self.assertEqual(merge_sort_dc([]), [])

    def test_quicksort(self) -> None:
        self.assertEqual(quicksort_dc([5, 3, 1, 4, 2, 8, 6]), [1, 2, 3, 4, 5, 6, 8])

    def test_quicksort_inplace(self) -> None:
        arr = [5, 3, 1, 4, 2]
        quicksort_inplace(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_closest_pair(self) -> None:
        self.assertAlmostEqual(closest_pair([1, 3, 6, 7, 11, 13]), 1.0)
        self.assertEqual(closest_pair([5]), float("inf"))
        self.assertAlmostEqual(closest_pair([1, 5]), 4.0)

    def test_strassen(self) -> None:
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        C = strassen_matrix_multiply(A, B)
        self.assertEqual(C, [[19, 22], [43, 50]])

    def test_karatsuba(self) -> None:
        self.assertEqual(karatsuba(12345, 6789), 12345 * 6789)
        self.assertEqual(karatsuba(0, 1234), 0)
        self.assertEqual(karatsuba(9, 9), 81)

    def test_find_max(self) -> None:
        self.assertEqual(find_max([3, 1, 4, 1, 5, 9, 2, 6]), 9)
        with self.assertRaises(ValueError):
            find_max([])

    def test_find_max_min(self) -> None:
        self.assertEqual(find_max_min([3, 1, 4, 1, 5, 9, 2, 6]), (1, 9))

    def test_power(self) -> None:
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(3, 0), 1)
        with self.assertRaises(ValueError):
            power(2, -1)

    def test_count_inversions(self) -> None:
        self.assertEqual(count_inversions([2, 4, 1, 3, 5]), 3)
        self.assertEqual(count_inversions([]), 0)
        self.assertEqual(count_inversions([1, 2, 3, 4]), 0)


# --------------------------------------------------------------------------- #
# String Algorithms
# --------------------------------------------------------------------------- #


class TestStringAlgorithms(unittest.TestCase):
    def test_rabin_karp(self) -> None:
        self.assertEqual(rabin_karp("abracadabra", "abra"), [0, 7])
        self.assertEqual(rabin_karp("aaaaa", "aa"), [0, 1, 2, 3])
        self.assertEqual(rabin_karp("abcdef", "xyz"), [])

    def test_kmp(self) -> None:
        self.assertEqual(kmp_search("ababcababcababcab", "ababc"), [0, 5, 10])
        self.assertEqual(kmp_search("aaaaa", "aa"), [0, 1, 2, 3])

    def test_naive(self) -> None:
        self.assertEqual(naive_string_match("hello world", "world"), [6])
        self.assertEqual(naive_string_match("abcabcabc", "abc"), [0, 3, 6])

    def test_z_algorithm(self) -> None:
        self.assertEqual(
            z_algorithm("aabxaayaab"), [0, 1, 0, 0, 2, 1, 0, 3, 1, 0]
        )
        self.assertEqual(z_algorithm("aaaa"), [0, 3, 2, 1])
        self.assertEqual(z_algorithm("abcd"), [0, 0, 0, 0])

    def test_longest_palindrome(self) -> None:
        # Both "bab" and "aba" are valid longest palindromes for "babad"; we
        # accept either. Also verify the result is actually a palindrome.
        for fn in (longest_palindromic_substring, manacher_palindromes):
            res = fn("babad")
            self.assertIn(res, ("bab", "aba"))
            self.assertEqual(res, res[::-1])
            self.assertEqual(fn("cbbd"), "bb")
            self.assertEqual(fn("racecar"), "racecar")
            self.assertEqual(fn(""), "")

    def test_anagram_check(self) -> None:
        self.assertTrue(anagram_check("listen", "silent"))
        self.assertFalse(anagram_check("hello", "world"))
        self.assertTrue(anagram_check("Astronomer", "Moon starer"))

    def test_run_length_encoding(self) -> None:
        self.assertEqual(run_length_encoding("aaabbc"), "3a2b1c")
        self.assertEqual(run_length_encoding("a"), "1a")
        self.assertEqual(run_length_encoding(""), "")


# --------------------------------------------------------------------------- #
# Number Theory
# --------------------------------------------------------------------------- #


class TestNumberTheory(unittest.TestCase):
    def test_sieve(self) -> None:
        self.assertEqual(sieve_of_eratosthenes(20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(sieve_of_eratosthenes(1), [])

    def test_is_prime(self) -> None:
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(0))

    def test_gcd_lcm(self) -> None:
        self.assertEqual(gcd(12, 18), 6)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(0, 5), 0)

    def test_modular_exponentiation(self) -> None:
        self.assertEqual(modular_exponentiation(2, 10, 1000), 24)
        # 3^117 mod 19 == 3^(117 mod 18) mod 19 == 3^9 mod 19 == 19683 mod 19 == 18
        self.assertEqual(modular_exponentiation(3, 117, 19), 18)
        self.assertEqual(modular_exponentiation(0, 5, 7), 0)
        self.assertEqual(modular_exponentiation(5, 0, 13), 1)

    def test_factorial(self) -> None:
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)

    def test_fibonacci(self) -> None:
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(10), 55)

    def test_prime_factorization(self) -> None:
        self.assertEqual(prime_factorization(360), {2: 3, 3: 2, 5: 1})
        self.assertEqual(prime_factorization(13), {13: 1})

    def test_euler_totient(self) -> None:
        self.assertEqual(euler_totient(1), 1)
        self.assertEqual(euler_totient(9), 6)
        self.assertEqual(euler_totient(36), 12)


if __name__ == "__main__":
    unittest.main()