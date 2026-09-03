"""Algorithms library.

A clean, well-documented collection of classic algorithms and data
structures implemented in pure Python (stdlib). Modules:

- :mod:`searching`
- :mod:`sorting`
- :mod:`graph_algorithms`
- :mod:`data_structures`
- :mod:`dynamic_programming`
- :mod:`greedy`
- :mod:`divide_and_conquer`
- :mod:`string_algorithms`
- :mod:`number_theory`

Re-exports the public API so callers can write e.g.::

    from Algorithms import binary_search, MinHeap, dijkstra
"""

from __future__ import annotations

# Re-export from each module so that ``from Algorithms import X`` works.
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

__all__ = [
    # searching
    "binary_search",
    "binary_search_recursive",
    "exponential_search",
    "interpolation_search",
    "jump_search",
    "linear_search",
    "ternary_search",
    # sorting
    "bubble_sort",
    "counting_sort",
    "heap_sort",
    "insertion_sort",
    "merge_sort",
    "quicksort",
    "radix_sort",
    "selection_sort",
    "shell_sort",
    # graph
    "a_star",
    "bellman_ford",
    "bfs",
    "dfs",
    "dfs_recursive",
    "dijkstra",
    "floyd_warshall",
    "kruskal_mst",
    "prim_mst",
    "topological_sort",
    # data structures
    "BinarySearchTree",
    "DoublyLinkedList",
    "Graph",
    "LRUCache",
    "LinkedList",
    "MaxHeap",
    "MinHeap",
    "Queue",
    "Stack",
    "Trie",
    "UnionFind",
    # dynamic programming
    "coin_change",
    "edit_distance",
    "fibonacci_memo",
    "fibonacci_tab",
    "knapsack_01",
    "knapsack_unbounded",
    "longest_common_substring",
    "longest_common_subsequence",
    "longest_increasing_subsequence",
    "matrix_chain_multiplication",
    "rod_cutting",
    "subset_sum",
    "word_break",
    # greedy
    "activity_selection",
    "fractional_knapsack",
    "gas_station_circuit",
    "huffman_coding",
    "job_sequencing",
    "minimum_coins",
    # divide & conquer
    "closest_pair",
    "count_inversions",
    "find_max",
    "find_max_min",
    "karatsuba",
    "merge_sort_dc",
    "power",
    "quicksort_dc",
    "quicksort_inplace",
    "strassen_matrix_multiply",
    # strings
    "anagram_check",
    "kmp_search",
    "longest_palindromic_substring",
    "manacher_palindromes",
    "naive_string_match",
    "rabin_karp",
    "run_length_encoding",
    "z_algorithm",
    # number theory
    "euler_totient",
    "factorial",
    "fibonacci",
    "gcd",
    "is_prime",
    "lcm",
    "modular_exponentiation",
    "prime_factorization",
    "sieve_of_eratosthenes",
]

__version__ = "1.0.0"