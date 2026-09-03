"""Algorithms library.

A clean, well-documented collection of classic and modern algorithms and
data structures implemented in pure Python (stdlib). Modules:

- :mod:`searching`
- :mod:`sorting`
- :mod:`graph_algorithms`
- :mod:`advanced_graph`
- :mod:`data_structures`
- :mod:`advanced_trees`
- :mod:`bloom_filter`
- :mod:`suffix_structures`
- :mod:`network_flow`
- :mod:`dynamic_programming`
- :mod:`advanced_dp`
- :mod:`greedy`
- :mod:`divide_and_conquer`
- :mod:`geometry`
- :mod:`string_algorithms`
- :mod:`number_theory`
- :mod:`randomized`

Re-exports the public API so callers can write e.g.::

    from Algorithms import binary_search, MinHeap, dijkstra, SegmentTree
"""

from __future__ import annotations

from .searching import (
    binary_search,
    binary_search_recursive,
    exponential_search,
    interpolation_search,
    jump_search,
    linear_search,
    ternary_search,
)
from .sorting import (
    bubble_sort,
    counting_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quicksort,
    radix_sort,
    selection_sort,
    shell_sort,
)
from .graph_algorithms import (
    a_star,
    bellman_ford,
    bfs,
    dfs,
    dfs_recursive,
    dijkstra,
    floyd_warshall,
    kruskal_mst,
    prim_mst,
    topological_sort,
)
from .advanced_graph import (
    connected_components,
    has_cycle_directed,
    has_cycle_undirected,
    johnson,
    kosaraju_scc,
    tarjan_scc,
    two_sat,
)
from .data_structures import (
    BinarySearchTree,
    DoublyLinkedList,
    Graph,
    LRUCache,
    LinkedList,
    MaxHeap,
    MinHeap,
    Queue,
    Stack,
    Trie,
    UnionFind,
)
from .advanced_trees import FenwickTree, SegmentTree, SkipList
from .bloom_filter import BloomFilter, CountingBloomFilter
from .suffix_structures import (
    SuffixAutomaton,
    build_lcp_array,
    build_suffix_array,
    suffix_array_search,
)
from .network_flow import (
    edmonds_karp,
    ford_fulkerson,
    hopcroft_karp,
    min_cut,
)
from .dynamic_programming import (
    coin_change,
    edit_distance,
    fibonacci_memo,
    fibonacci_tab,
    knapsack_01,
    knapsack_unbounded,
    longest_common_substring,
    longest_common_subsequence,
    longest_increasing_subsequence,
    matrix_chain_multiplication,
    rod_cutting,
    subset_sum,
    word_break,
)
from .advanced_dp import (
    boolean_parenthesization,
    digit_dp,
    is_palindrome,
    longest_palindromic_subsequence,
    longest_path_dag,
    tsp_held_karp,
    weighted_interval_scheduling,
)
from .greedy import (
    activity_selection,
    fractional_knapsack,
    gas_station_circuit,
    huffman_coding,
    job_sequencing,
    minimum_coins,
)
from .divide_and_conquer import (
    closest_pair,
    count_inversions,
    find_max,
    find_max_min,
    karatsuba,
    merge_sort as merge_sort_dc,
    power,
    quicksort as quicksort_dc,
    quicksort_inplace,
    strassen_matrix_multiply,
)
from .geometry import (
    closest_pair_2d,
    convex_hull_graham_scan,
    count_line_intersections,
)
from .string_algorithms import (
    anagram_check,
    kmp_search,
    longest_palindromic_substring,
    manacher_palindromes,
    naive_string_match,
    rabin_karp,
    run_length_encoding,
    z_algorithm,
)
from .number_theory import (
    euler_totient,
    factorial,
    fibonacci,
    gcd,
    is_prime,
    lcm,
    modular_exponentiation,
    prime_factorization,
    sieve_of_eratosthenes,
)
from .randomized import (
    Treap,
    fisher_yates_shuffle,
    miller_rabin,
    monte_carlo_pi,
    quickselect,
    reservoir_sample,
)

__all__ = [
    # searching
    "binary_search", "binary_search_recursive", "exponential_search",
    "interpolation_search", "jump_search", "linear_search", "ternary_search",
    # sorting
    "bubble_sort", "counting_sort", "heap_sort", "insertion_sort", "merge_sort",
    "quicksort", "radix_sort", "selection_sort", "shell_sort",
    # graph
    "a_star", "bellman_ford", "bfs", "dfs", "dfs_recursive", "dijkstra",
    "floyd_warshall", "kruskal_mst", "prim_mst", "topological_sort",
    # advanced graph
    "connected_components", "has_cycle_directed", "has_cycle_undirected",
    "johnson", "kosaraju_scc", "tarjan_scc", "two_sat",
    # data structures
    "BinarySearchTree", "DoublyLinkedList", "Graph", "LRUCache", "LinkedList",
    "MaxHeap", "MinHeap", "Queue", "Stack", "Trie", "UnionFind",
    # advanced trees
    "FenwickTree", "SegmentTree", "SkipList",
    # bloom filter
    "BloomFilter", "CountingBloomFilter",
    # suffix structures
    "SuffixAutomaton", "build_lcp_array", "build_suffix_array",
    "suffix_array_search",
    # network flow
    "edmonds_karp", "ford_fulkerson", "hopcroft_karp", "min_cut",
    # dynamic programming
    "coin_change", "edit_distance", "fibonacci_memo", "fibonacci_tab",
    "knapsack_01", "knapsack_unbounded", "longest_common_substring",
    "longest_common_subsequence", "longest_increasing_subsequence",
    "matrix_chain_multiplication", "rod_cutting", "subset_sum", "word_break",
    # advanced DP
    "boolean_parenthesization", "digit_dp", "is_palindrome",
    "longest_palindromic_subsequence", "longest_path_dag", "tsp_held_karp",
    "weighted_interval_scheduling",
    # greedy
    "activity_selection", "fractional_knapsack", "gas_station_circuit",
    "huffman_coding", "job_sequencing", "minimum_coins",
    # divide & conquer
    "closest_pair", "count_inversions", "find_max", "find_max_min",
    "karatsuba", "merge_sort_dc", "power", "quicksort_dc", "quicksort_inplace",
    "strassen_matrix_multiply",
    # geometry
    "closest_pair_2d", "convex_hull_graham_scan", "count_line_intersections",
    # strings
    "anagram_check", "kmp_search", "longest_palindromic_substring",
    "manacher_palindromes", "naive_string_match", "rabin_karp",
    "run_length_encoding", "z_algorithm",
    # number theory
    "euler_totient", "factorial", "fibonacci", "gcd", "is_prime", "lcm",
    "modular_exponentiation", "prime_factorization", "sieve_of_eratosthenes",
    # randomized
    "Treap", "fisher_yates_shuffle", "miller_rabin", "monte_carlo_pi",
    "quickselect", "reservoir_sample",
]

__version__ = "2.0.0"