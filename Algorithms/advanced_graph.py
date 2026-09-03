"""Additional graph algorithms: cycle detection, connected components,
strongly connected components (Tarjan / Kosaraju), Johnson's all-pairs,
maximum bipartite matching variants.

References:
    - Tarjan, R. E. (1972). "Depth-first search and linear graph
      algorithms". SIAM Journal on Computing.
    - Kosaraju, S. R. (1978). Unpublished; described in CLRS.
    - Johnson, D. B. (1977). "Efficient algorithms for shortest paths in
      sparse networks". JACM.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Hashable, TypeVar

N = TypeVar("N", bound=Hashable)


# --------------------------------------------------------------------------- #
# Cycle detection and connectivity
# --------------------------------------------------------------------------- #


def has_cycle_undirected(graph: dict[N, list[N]]) -> bool:
    """Detect whether an undirected graph contains a cycle.

    Args:
        graph: Undirected adjacency ``{u: [v, ...]}`` (edges listed twice
            are OK; we treat each edge once).

    Returns:
        True if a cycle exists, False otherwise.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[N, int] = {n: WHITE for n in graph}

    for start in graph:
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack: list[tuple[N, N | None]] = [(start, None)]
        while stack:
            node, parent = stack.pop()
            for nbr in graph[node]:
                if color.get(nbr, WHITE) == GRAY and nbr != parent:
                    return True
                if color.get(nbr, WHITE) == WHITE:
                    color[nbr] = GRAY
                    stack.append((nbr, node))
            color[node] = BLACK
    return False


def has_cycle_directed(graph: dict[N, list[N]]) -> bool:
    """Detect cycle in a directed graph via DFS colouring.

    Args:
        graph: Directed adjacency ``{u: [v, ...]}``.

    Returns:
        True if a directed cycle exists.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[N, int] = {n: WHITE for n in graph}
    for start in graph:
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack: list[tuple[N, bool]] = [(start, True)]
        while stack:
            node, expand = stack.pop()
            if not expand:
                color[node] = BLACK
                continue
            stack.append((node, False))
            for nbr in graph[node]:
                if color.get(nbr, WHITE) == GRAY:
                    return True
                if color.get(nbr, WHITE) == WHITE:
                    color[nbr] = GRAY
                    stack.append((nbr, True))
    return False


def connected_components(graph: dict[N, list[N]]) -> list[set[N]]:
    """Connected components in an UNDIRECTED graph.

    Args:
        graph: Undirected adjacency.

    Returns:
        List of connected components (each a set of nodes).

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    seen: set[N] = set()
    components: list[set[N]] = []
    for start in graph:
        if start in seen:
            continue
        component: set[N] = set()
        q = deque([start])
        seen.add(start)
        while q:
            u = q.popleft()
            component.add(u)
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        components.append(component)
    return components


# --------------------------------------------------------------------------- #
# Strongly connected components (Tarjan + Kosaraju)
# --------------------------------------------------------------------------- #


def tarjan_scc(graph: dict[N, list[N]]) -> list[list[N]]:
    """Strongly connected components via Tarjan's algorithm (1972).

    Args:
        graph: Directed adjacency ``{u: [v, ...]}``.

    Returns:
        List of SCCs. Nodes appear in some SCC; isolated nodes are SCCs
        of size 1.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    index_counter = [0]
    stack: list[N] = []
    lowlinks: dict[N, int] = {}
    index: dict[N, int] = {}
    on_stack: dict[N, bool] = {n: False for n in graph}
    sccs: list[list[N]] = []

    def strongconnect(node: N) -> None:
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack[node] = True

        for successor in graph.get(node, []):
            if successor not in index:
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node], lowlinks[successor])
            elif on_stack.get(successor, False):
                lowlinks[node] = min(lowlinks[node], index[successor])

        if lowlinks[node] == index[node]:
            scc: list[N] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    for n in list(graph):
        if n not in index:
            strongconnect(n)
    return sccs


def kosaraju_scc(graph: dict[N, list[N]]) -> list[list[N]]:
    """Strongly connected components via Kosaraju's algorithm.

    Steps:
        1. DFS on G, push nodes onto a stack in finish-time order.
        2. Build G^T (reverse edges).
        3. Pop nodes off the stack; for each unvisited node, DFS on G^T
           collects one SCC.

    Args:
        graph: Directed adjacency ``{u: [v, ...]}``.

    Returns:
        List of SCCs.

    Complexity:
        Time: O(V + E). Space: O(V + E).
    """
    visited: set[N] = set()
    order: list[N] = []

    # Pass 1: DFS order
    def dfs1(u: N) -> None:
        stack = [(u, iter(graph.get(u, [])))]
        visited.add(u)
        while stack:
            node, it = stack[-1]
            try:
                nxt = next(it)
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append((nxt, iter(graph.get(nxt, []))))
            except StopIteration:
                order.append(node)
                stack.pop()

    for n in list(graph):
        if n not in visited:
            dfs1(n)

    # Pass 2: DFS on transpose graph
    reverse: dict[N, list[N]] = {n: [] for n in graph}
    for u in graph:
        for v in graph[u]:
            reverse.setdefault(v, []).append(u)

    visited2: set[N] = set()
    sccs: list[list[N]] = []
    for start in reversed(order):
        if start in visited2:
            continue
        component: list[N] = []
        stack = [start]
        visited2.add(start)
        while stack:
            u = stack.pop()
            component.append(u)
            for v in reverse.get(u, []):
                if v not in visited2:
                    visited2.add(v)
                    stack.append(v)
        sccs.append(component)
    return sccs


# --------------------------------------------------------------------------- #
# Johnson's algorithm: all-pairs shortest paths with negative weights
# --------------------------------------------------------------------------- #


def johnson(
    graph: dict[N, dict[N, float]], nodes: list[N]
) -> dict[N, dict[N, float]]:
    """Johnson's all-pairs shortest paths (1977).

    Re-weights edges via Bellman-Ford from a virtual source, then runs
    Dijkstra from every node. Handles negative weights (no negative
    cycles).

    Args:
        graph: Weighted adjacency dict ``{u: {v: weight}}``.
        nodes: All nodes in the graph (including those with no outgoing edges).

    Returns:
        Nested dict ``dist[u][v] = shortest distance``; ``float('inf')``
        if unreachable.

    Raises:
        ValueError: If the graph has a negative-weight cycle.

    Complexity:
        Time: O(V * E + V * E * log V). Space: O(V^2).
    """
    # Step 1: add virtual source, run Bellman-Ford.
    s = object()  # unique sentinel
    augmented: dict[object, dict[object, float]] = {s: {n: 0 for n in nodes}}
    for u in nodes:
        augmented[u] = dict(graph.get(u, {}))
    for u in nodes:
        augmented.setdefault(u, {})

    # Bellman-Ford
    h: dict[object, float] = {n: 0 for n in nodes}
    h[s] = 0
    total_nodes = list(augmented.keys())
    for _ in range(len(total_nodes) - 1):
        updated = False
        for u in augmented:
            for v, w in augmented[u].items():
                if h[u] + w < h.get(v, float("inf")):
                    h[v] = h[u] + w
                    updated = True
        if not updated:
            break
    for u in augmented:
        for v, w in augmented[u].items():
            if h[u] + w < h.get(v, float("inf")):
                raise ValueError("Graph contains a negative-weight cycle")

    # Step 2: re-weight and run Dijkstra from each node
    reweighted: dict[N, dict[N, float]] = {}
    for u in nodes:
        reweighted[u] = {}
        for v, w in graph.get(u, {}).items():
            new_w = w + h[u] - h.get(v, 0)
            reweighted[u][v] = new_w

    all_dist: dict[N, dict[N, float]] = {}
    for u in nodes:
        # Dijkstra on reweighted graph.
        dist: dict[N, float] = {u: 0}
        pq: list[tuple[float, N]] = [(0, u)]
        while pq:
            d, x = heapq.heappop(pq)
            if d > dist.get(x, float("inf")):
                continue
            for v, w in reweighted.get(x, {}).items():
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        # Re-derive original distances: d_orig(u,v) = d_reweighted(u,v) - h[u] + h[v]
        for v in dist:
            dist[v] = dist[v] - h[u] + h.get(v, 0)
        all_dist[u] = dist
    return all_dist


# --------------------------------------------------------------------------- #
# 2-SAT
# --------------------------------------------------------------------------- #


def two_sat(n_vars: int, clauses: list[tuple[int, int]]) -> list[bool] | None:
    """Solve 2-SAT via Kosaraju's SCC.

    Args:
        n_vars: Number of variables, labelled 0..n_vars-1.
        clauses: List of ``(literal_i, literal_j)`` where literal is
            ``k`` for ``x_k = True`` and ``~k`` for ``k + n_vars`` for
            ``x_k = False`` (i.e. literal ``l`` represents ``x_l`` if
            ``l < n_vars`` else ``~x_{l - n_vars}``).

    Returns:
        List of boolean assignments (length ``n_vars``) if satisfiable;
        None otherwise.

    Complexity:
        Time: O(V + E) where V = 2 * n_vars. Space: O(V + E).
    """
    n = n_vars * 2  # node 0..2n-1: node i is literal i, node i+n is NOT i.

    def var(lit: int) -> int:
        return lit % n_vars

    def neg(lit: int) -> int:
        return (lit + n_vars) % n

    g: dict[int, list[int]] = {i: [] for i in range(n)}
    rg: dict[int, list[int]] = {i: [] for i in range(n)}
    for a, b in clauses:
        # (a OR b) -> (!a -> b) AND (!b -> a)
        na, nb = neg(a), neg(b)
        g[na].append(b)
        g[nb].append(a)
        rg[b].append(na)
        rg[a].append(nb)

    # Kosaraju
    visited: set[int] = set()
    order: list[int] = []

    def dfs1(start: int) -> None:
        stack = [(start, iter(g[start]))]
        visited.add(start)
        while stack:
            node, it = stack[-1]
            try:
                nxt = next(it)
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append((nxt, iter(g[nxt])))
            except StopIteration:
                order.append(node)
                stack.pop()

    for i in range(n):
        if i not in visited:
            dfs1(i)

    comp: dict[int, int] = {}
    scc_id = 0
    for u in reversed(order):
        if u in comp:
            continue
        stack = [u]
        comp[u] = scc_id
        while stack:
            x = stack.pop()
            for v in rg[x]:
                if v not in comp:
                    comp[v] = scc_id
                    stack.append(v)
        scc_id += 1

    assignment: list[bool] = [False] * n_vars
    for i in range(n_vars):
        if comp.get(i) == comp.get(i + n_vars):
            return None
        assignment[i] = comp.get(i, -1) > comp.get(i + n_vars, -1)
    return assignment


__all__ = [
    "has_cycle_undirected",
    "has_cycle_directed",
    "connected_components",
    "tarjan_scc",
    "kosaraju_scc",
    "johnson",
    "two_sat",
]