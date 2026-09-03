# Algorithms

A clean, well-documented collection of classic algorithms and data structures
implemented in pure Python (standard library only — no external dependencies).

The library lives inside the `Algorithms/` package; the repository root also
contains problem-solution files (`P1.py`, `P2.py`, `P3.py`, `P4.py`) and a
dedicated `Sorting_Algorithms.py` from earlier coursework.

## Table of Contents

- [Quick Start](#quick-start)
- [Modules](#modules)
  - [Searching](#searching)
  - [Sorting](#sorting)
  - [Graph Algorithms](#graph-algorithms)
  - [Data Structures](#data-structures)
  - [Dynamic Programming](#dynamic-programming)
  - [Greedy](#greedy)
  - [Divide & Conquer](#divide--conquer)
  - [String Algorithms](#string-algorithms)
  - [Number Theory](#number-theory)
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
)

# Find an element in a sorted array
idx = binary_search([1, 3, 5, 7, 9], 5)  # -> 2

# Sort a list (returns a new list)
sorted_arr = merge_sort([5, 3, 1, 4, 2])  # -> [1, 2, 3, 4, 5]

# Shortest paths in a weighted graph
graph = {
    "A": {"B": 4, "C": 1},
    "B": {"C": 2, "D": 5},
    "C": {"D": 8},
    "D": {},
}
distances = dijkstra(graph, "A")  # -> {"A": 0, "B": 4, "C": 1, "D": 9}

# A min-heap
h = MinHeap([5, 3, 8, 1])
while h.size() > 0:
    print(h.pop())  # 1, 3, 5, 8

# 0/1 knapsack
best = knapsack_01(weights=[2, 3, 4, 5], values=[3, 4, 5, 6], capacity=5)
# -> 7
```

## Modules

### Searching

| Function | Description | Time | Space |
| --- | --- | --- | --- |
| `linear_search` | Linear scan of arbitrary sequence | O(n) | O(1) |
| `binary_search` | Iterative binary search on sorted seq | O(log n) | O(1) |
| `binary_search_recursive` | Recursive binary search | O(log n) | O(log n) |
| `ternary_search` | Splits range into three | O(log₃ n) | O(1) |
| `jump_search` | Block-jump then linear | O(√n) | O(1) |
| `interpolation_search` | Estimated position from value | O(log log n) avg | O(1) |
| `exponential_search` | Gallop then binary | O(log n) | O(1) |

### Sorting

| Function | Description | Time | Space | Stable |
| --- | --- | --- | --- | --- |
| `bubble_sort` | Bubble sort with early-exit | O(n²) | O(1) | Yes |
| `selection_sort` | Selection sort | O(n²) | O(1) | No |
| `insertion_sort` | Insertion sort | O(n²) | O(1) | Yes |
| `merge_sort` | Top-down merge sort | O(n log n) | O(n) | Yes |
| `quicksort` | Functional quicksort | O(n log n) avg | O(n) | No |
| `heap_sort` | In-place heap sort | O(n log n) | O(1) | No |
| `shell_sort` | Shell sort with halving gaps | O(n^1.25–n²) | O(1) | No |
| `counting_sort` | Non-negative int sort | O(n + k) | O(n + k) | Yes |
| `radix_sort` | LSD radix sort | O(n · d) | O(n) | Yes |

### Graph Algorithms

Graph format used throughout: `graph[u][v] = weight` (use `{}` for unweighted).

| Function | Description | Time | Space |
| --- | --- | --- | --- |
| `bfs` | Breadth-first traversal | O(V + E) | O(V) |
| `dfs` / `dfs_recursive` | Depth-first traversal | O(V + E) | O(V) |
| `dijkstra` | Single-source shortest paths (≥ 0 weights) | O((V+E) log V) | O(V) |
| `bellman_ford` | Single-source shortest paths (any weights) | O(V · E) | O(V) |
| `floyd_warshall` | All-pairs shortest paths | O(V³) | O(V²) |
| `topological_sort` | Kahn's algorithm | O(V + E) | O(V) |
| `kruskal_mst` | Kruskal MST (Union-Find) | O(E log E) | O(V + E) |
| `prim_mst` | Prim MST (heap) | O(E log V) | O(V) |
| `a_star` | A* shortest-path search | O(E log V) | O(V) |

### Data Structures

| Class | Description |
| --- | --- |
| `Stack` | LIFO stack |
| `Queue` | FIFO queue (deque-backed) |
| `LinkedList` | Singly linked list |
| `DoublyLinkedList` | Doubly linked list with O(1) head/tail |
| `BinarySearchTree` | BST with insert / search / delete |
| `Trie` | Prefix tree for strings |
| `MinHeap` / `MaxHeap` | Binary heaps with heapify |
| `UnionFind` | DSU with path compression + union by rank |
| `Graph` | Adjacency-list graph with BFS/DFS |
| `LRUCache` | LRU cache (OrderedDict-backed) |

### Dynamic Programming

| Function | Description |
| --- | --- |
| `fibonacci_memo` / `fibonacci_tab` | Fibonacci numbers |
| `coin_change` | Min coins for amount |
| `longest_common_subsequence` / `longest_common_substring` | LCS variants |
| `edit_distance` | Levenshtein distance |
| `knapsack_01` / `knapsack_unbounded` | Knapsack variants |
| `longest_increasing_subsequence` | LIS in O(n log n) |
| `matrix_chain_multiplication` | Min scalar multiplications |
| `subset_sum` | Subset-sum decision |
| `rod_cutting` | Max revenue cutting rod |
| `word_break` | Dictionary word segmentation |

### Greedy

| Function | Description |
| --- | --- |
| `activity_selection` | Earliest-finish-time activity picker |
| `fractional_knapsack` | Fractional knapsack |
| `huffman_coding` | Optimal prefix-free codes |
| `job_sequencing` | Unit-time job scheduling |
| `minimum_coins` | Greedy min coins (canonical systems) |
| `gas_station_circuit` | Circular gas-station tour |

### Divide & Conquer

| Function | Description | Time |
| --- | --- | --- |
| `merge_sort` (D&C version) | Merge sort | O(n log n) |
| `quicksort` (D&C version) | Functional quicksort | O(n log n) avg |
| `quicksort_inplace` | In-place quicksort | O(n log n) avg |
| `closest_pair` | 1-D closest pair | O(n log n) |
| `strassen_matrix_multiply` | Strassen matrix product | O(n^log₂7) |
| `karatsuba` | Big-int multiplication | O(n^log₂3) |
| `find_max` / `find_max_min` | Min/max in ~3n/2 comparisons | O(n) |
| `power` | Fast exponentiation | O(log n) |
| `count_inversions` | Inversion count via merge | O(n log n) |

### String Algorithms

| Function | Description | Time |
| --- | --- | --- |
| `rabin_karp` | Rolling-hash search | O(n + m) avg |
| `kmp_search` | Knuth-Morris-Pratt | O(n + m) |
| `naive_string_match` | Brute-force search | O(n · m) |
| `z_algorithm` | Z-array in O(n) | O(n) |
| `longest_palindromic_substring` | Expand-around-centers | O(n²) |
| `manacher_palindromes` | Manacher's algorithm | O(n) |
| `anagram_check` | Counter-based anagram test | O(n) |
| `run_length_encoding` | RLE encoding | O(n) |

### Number Theory

| Function | Description | Time |
| --- | --- | --- |
| `sieve_of_eratosthenes` | All primes ≤ n | O(n log log n) |
| `is_prime` | Trial-division primality | O(√n) |
| `gcd` / `lcm` | Euclidean gcd / lcm | O(log min(a, b)) |
| `modular_exponentiation` | Fast modular exponentiation | O(log e) |
| `factorial` | Iterative factorial | O(n) |
| `fibonacci` | Naive recursive Fibonacci | O(2ⁿ) |
| `prime_factorization` | Factor by trial division | O(√n) |
| `euler_totient` | φ(n) | O(√n) |

## Running Tests

From the repository root:

```bash
python -m unittest Algorithms.tests -v
```

Or from inside the `Algorithms/` subdirectory:

```bash
python tests.py
```

There are **88 unit tests** covering every algorithm with edge cases (empty
input, single element, duplicates, large random data).

Latest run:

```
Ran 88 tests in 0.020s
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
    ├── data_structures.py
    ├── dynamic_programming.py
    ├── greedy.py
    ├── divide_and_conquer.py
    ├── string_algorithms.py
    ├── number_theory.py
    ├── tests.py           # 88 unittest cases
    ├── requirements.txt   # Standard library only
    └── README.md          # This file
```

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
  *Introduction to Algorithms* (3rd ed.). MIT Press.
- Skiena, S. S. (2008). *The Algorithm Design Manual*. Springer.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.