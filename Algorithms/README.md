# Algorithms

A clean, well-documented collection of classic and modern algorithms and
data structures implemented in pure Python (standard library only — no
external dependencies).

The library lives inside the `Algorithms/` package; the repository root
also contains problem-solution files (`P1.py`, `P2.py`, `P3.py`, `P4.py`)
and a dedicated `Sorting_Algorithms.py` from earlier coursework.

## Table of Contents

- [Quick Start](#quick-start)
- [Modules](#modules)
- [Running Tests](#running-tests)
- [Project Layout](#project-layout)
- [References](#references)

## Quick Start

```python
from Algorithms import (
    binary_search,
    merge_sort,
    dijkstra,
    MinHeap,
    knapsack_01,
    fibonacci_memo,
    closest_pair,
    rabin_karp,
    sieve_of_eratosthenes,
    SegmentTree,        # range queries
    SuffixAutomaton,    # substring queries
    BloomFilter,        # probabilistic set
    tsp_held_karp,      # exact TSP
    convex_hull_graham_scan,
    miller_rabin,       # randomized primality
)
```

## Modules

### Searching (`searching.py`)
Linear, binary, ternary, jump, interpolation, exponential search.

### Sorting (`sorting.py`)
Bubble, selection, insertion, merge, quick, heap, shell, counting, radix.

### Graph Algorithms (`graph_algorithms.py`, `advanced_graph.py`)
- `graph_algorithms.py`: BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall,
  topological sort, Kruskal MST, Prim MST, A*.
- `advanced_graph.py`: cycle detection (undirected/directed), connected
  components, **Tarjan** and **Kosaraju** strongly connected components,
  **Johnson's** all-pairs shortest paths, **2-SAT** solver.

### Data Structures (`data_structures.py`, `advanced_trees.py`, `bloom_filter.py`)
- `data_structures.py`: Stack, Queue, LinkedList, DoublyLinkedList, BST,
  Trie, Min/MaxHeap, UnionFind, Graph, LRU cache.
- `advanced_trees.py`: **Segment tree** (range queries), **Fenwick tree**
  (Binary Indexed Tree), **Skip list** (Pugh 1990).
- `bloom_filter.py`: Standard and **counting Bloom filters**.

### Suffix Structures (`suffix_structures.py`)
**Suffix array** (doubling algorithm, O(n log n)), **LCP array** (Kasai),
suffix array search, and a full **suffix automaton** (SAM) supporting
O(|pattern|) substring queries.

### Network Flow (`network_flow.py`)
**Ford-Fulkerson / Edmonds-Karp** maximum flow, **min s-t cut** (by duality),
**Hopcroft-Karp** maximum bipartite matching.

### Dynamic Programming (`dynamic_programming.py`, `advanced_dp.py`)
- `dynamic_programming.py`: Fibonacci, coin change, LCS, edit distance,
  knapsack, LIS, matrix chain, subset sum, rod cutting, word break.
- `advanced_dp.py`: **Held-Karp TSP** (O(n² · 2ⁿ)), **longest palindromic
  subsequence**, **longest path in a DAG**, **weighted interval scheduling**,
  **boolean parenthesization**, **digit DP**.

### Greedy (`greedy.py`)
Activity selection, fractional knapsack, Huffman coding, job sequencing,
minimum coins, online paging.

### Divide & Conquer (`divide_and_conquer.py`)
Merge sort, quicksort, closest pair, **Strassen matrix multiplication**,
**Karatsuba** big-int multiplication, find max/min, fast power, count
    inversions.

### Geometry (`geometry.py`)
**Convex hull** (Graham scan), **2-D closest pair** (Shamos 1978),
line-sweep intersection count.

### String Algorithms (`string_algorithms.py`)
Rabin-Karp, KMP, naive, Z-algorithm, Manacher palindromes, anagram check,
run-length encoding.

### Number Theory (`number_theory.py`)
Sieve of Eratosthenes, primality, gcd/lcm, modular exponentiation,
factorial, Fibonacci, prime factorisation, Euler totient.

### Randomized (`randomized.py`)
**Reservoir sampling** (Vitter 1985), Fisher-Yates shuffle, **quickselect**
(Hoare), **Miller-Rabin** primality, Monte-Carlo pi estimation, **Treap**
(randomised BST).

## Running Tests

From the repository root:

```bash
python -m unittest Algorithms.tests Algorithms.tests_v2 -v
```

Or from inside the `Algorithms/` subdirectory:

```bash
python tests.py
python tests_v2.py
```

There are **130 unit tests** covering every algorithm with edge cases
(empty input, single element, duplicates, large random data).

Latest run:

```
Ran 130 tests in 0.021s
OK
```

## Project Layout

```
Algorithms/
├── P1.py                  # Queues: Array, SLL, DLL (coursework)
├── P2.py                  # Sorting benchmarks (coursework)
├── P3.py                  # AVL tree with closest search (coursework)
├── P4.py                  # Multi-objective Dijkstra (coursework)
├── Sorting_Algorithms.py  # Initial sorting module (coursework)
└── Algorithms/            # The library package
    ├── __init__.py        # Public re-exports
    ├── searching.py
    ├── sorting.py
    ├── graph_algorithms.py
    ├── advanced_graph.py
    ├── data_structures.py
    ├── advanced_trees.py
    ├── bloom_filter.py
    ├── suffix_structures.py
    ├── network_flow.py
    ├── dynamic_programming.py
    ├── advanced_dp.py
    ├── greedy.py
    ├── divide_and_conquer.py
    ├── geometry.py
    ├── string_algorithms.py
    ├── number_theory.py
    ├── randomized.py
    ├── tests.py           # 88 unit tests
    ├── tests_v2.py        # 42 additional tests for new modules
    ├── requirements.txt   # Standard library only
    └── README.md          # This file
```

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
  *Introduction to Algorithms* (3rd ed.). MIT Press.
- Skiena, S. S. (2008). *The Algorithm Design Manual*. Springer.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.

### arXiv papers inspiring newer additions

- **arXiv:2401.04509** — Inenaga, "Linear-size Suffix Tries and
  Linear-size CDAWGs Simplified and Improved" → suffix structures.
- **arXiv:2401.02647** — Dozier, Salamatian, Rubenstein, "Modeling
  Average False Positive Rates of Recycling Bloom Filters" →
  Bloom filter implementation.
- **arXiv:2401.05627** — Henzinger, Li, Rao, Wang, "Deterministic
  Near-Linear Time Minimum Cut in Weighted Graphs" → flow / min-cut.
- **arXiv:2401.07467** — Wynn et al., "Selection Improvements on
  Parallel Iterative Algorithm for Stable Matching".
- **arXiv:2401.05834** — Mari et al., "Modeling Online Paging in
  Multi-Core Systems" → LRU cache.
- Recent submissions (Sep 2026) on cs.DS for further reading.