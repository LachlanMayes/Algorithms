# Algorithms

A Python algorithms library by [LachlanMayes](https://github.com/LachlanMayes).

## What's in here

- **`Algorithms/`** — A clean, well-tested Python library of classic and
  modern algorithms and data structures. v2.0 adds suffix structures
  (suffix array, suffix automaton), Bloom filters, segment/Fenwick trees,
  skip lists, network flow, advanced DP (Held-Karp TSP, digit DP, etc.),
  randomised algorithms (reservoir sampling, Miller-Rabin, Treap), and
  computational geometry (convex hull, 2-D closest pair). Pure stdlib,
  130 unit tests, full type hints and docstrings.

- **`P1.py`, `P2.py`, `P3.py`, `P4.py`** — Coursework problem solutions
  covering queue implementations, sorting benchmarks, an AVL tree with
  closest-search, and multi-objective Dijkstra routing.

- **`Sorting_Algorithms.py`** — Standalone sorting implementations (the
  earlier version of the library).

## Quick start

```bash
# Clone
git clone https://github.com/LachlanMayes/Algorithms.git
cd Algorithms

# Run the test suite (from repo root)
python -m unittest Algorithms.tests Algorithms.tests_v2 -v
```

See [`Algorithms/README.md`](Algorithms/README.md) for the full API,
complexity tables, usage examples, and references to arXiv papers.

## Status

```
Ran 130 tests in 0.021s
OK
```