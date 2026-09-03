"""Graph algorithms.

Graph format used throughout this module:

- Weighted directed graph: ``graph[u]`` is a dict mapping neighbour ``v`` to edge
  weight ``w``. Example::

      {
          "A": {"B": 4, "C": 8},
          "B": {"C": 2, "D": 5},
          ...
      }

- Unweighted: the same format with all weights == 1, or pass ``{}`` (empty dict)
  as the weight for each neighbour; the algorithms only require the keys.

- Edge list: ``edges`` is a list of ``(u, v, w)`` tuples (used by Kruskal).

Nodes may be any hashable type (str, int, tuple).
"""

from __future__ import annotations

import heapq
from typing import Callable, Hashable, Iterable, TypeVar

N = TypeVar("N", bound=Hashable)


def bfs(graph: dict[N, dict[N, float]], start: N) -> list[N]:
    """Breadth-first traversal from ``start``.

    Args:
        graph: Adjacency dict ``{u: {v: weight}}``.
        start: Source node.

    Returns:
        Nodes in BFS visit order.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    from collections import deque

    visited = []
    queue = deque([start])
    seen = {start}
    while queue:
        node = queue.popleft()
        visited.append(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return visited


def dfs(graph: dict[N, dict[N, float]], start: N) -> list[N]:
    """Iterative depth-first traversal from ``start``.

    Args:
        graph: Adjacency dict ``{u: {v: weight}}``.
        start: Source node.

    Returns:
        Nodes in DFS visit order.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    visited = []
    stack = [start]
    seen = {start}
    while stack:
        node = stack.pop()
        visited.append(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return visited


def dfs_recursive(
    graph: dict[N, dict[N, float]],
    start: N,
    visited: set[N] | None = None,
) -> list[N]:
    """Recursive depth-first traversal from ``start``.

    Args:
        graph: Adjacency dict ``{u: {v: weight}}``.
        start: Source node.
        visited: Set of already-visited nodes (used internally by recursion).

    Returns:
        Nodes in DFS visit order.

    Complexity:
        Time: O(V + E). Space: O(V) recursion stack.
    """
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in graph.get(start, {}):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    return order


def dijkstra(graph: dict[N, dict[N, float]], start: N) -> dict[N, float]:
    """Single-source shortest paths with non-negative weights.

    Args:
        graph: Weighted adjacency dict.
        start: Source node.

    Returns:
        Mapping ``{node: shortest_distance_from_start}``. Unreachable nodes
        are absent.

    Raises:
        ValueError: If a negative edge weight is encountered.

    Complexity:
        Time: O((V + E) log V). Space: O(V).
    """
    for u in graph:
        for v, w in graph[u].items():
            if w < 0:
                raise ValueError(f"Dijkstra requires non-negative weights (edge {u}->{v} = {w})")

    dist: dict[N, float] = {start: 0}
    pq: list[tuple[float, N]] = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in graph.get(u, {}).items():
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def bellman_ford(graph: dict[N, dict[N, float]], start: N) -> dict[N, float]:
    """Single-source shortest paths allowing negative edges.

    Args:
        graph: Weighted adjacency dict.
        start: Source node.

    Returns:
        Mapping ``{node: shortest_distance_from_start}``.

    Raises:
        ValueError: If a negative-weight cycle is reachable from ``start``.

    Complexity:
        Time: O(V * E). Space: O(V).
    """
    nodes: set[N] = set(graph.keys())
    for u in graph:
        nodes.update(graph[u].keys())

    dist: dict[N, float] = {node: float("inf") for node in nodes}
    dist[start] = 0

    for _ in range(len(nodes) - 1):
        updated = False
        for u in graph:
            for v, w in graph[u].items():
                if dist[u] + w < dist.get(v, float("inf")):
                    dist[v] = dist[u] + w
                    updated = True
        if not updated:
            break

    # Negative-cycle detection
    for u in graph:
        for v, w in graph[u].items():
            if dist[u] + w < dist.get(v, float("inf")):
                raise ValueError("Graph contains a negative-weight cycle")

    return dist


def floyd_warshall(graph: dict[N, dict[N, float]]) -> dict[N, dict[N, float]]:
    """All-pairs shortest paths.

    Args:
        graph: Weighted adjacency dict.

    Returns:
        2-D mapping ``dist[u][v]`` of shortest path distance from u to v.
        ``float('inf')`` means unreachable; ``0`` means u == v.

    Complexity:
        Time: O(V^3). Space: O(V^2).
    """
    nodes: list[N] = list(graph.keys())
    for u in graph:
        for v in graph[u]:
            if v not in nodes:
                nodes.append(v)

    dist: dict[N, dict[N, float]] = {
        u: {v: float("inf") for v in nodes} for u in nodes
    }
    for u in nodes:
        dist[u][u] = 0
        for v, w in graph.get(u, {}).items():
            dist[u][v] = w

    for k in nodes:
        for i in nodes:
            dik = dist[i][k]
            if dik == float("inf"):
                continue
            row_i = dist[i]
            row_k = dist[k]
            for j in nodes:
                new = dik + row_k[j]
                if new < row_i[j]:
                    row_i[j] = new
    return dist


def topological_sort(graph: dict[N, dict[N, float]]) -> list[N]:
    """Kahn's algorithm: topological order of a DAG.

    Args:
        graph: Adjacency dict (edge weights are ignored).

    Returns:
        Topologically sorted list of nodes.

    Raises:
        ValueError: If the graph contains a cycle.

    Complexity:
        Time: O(V + E). Space: O(V).
    """
    nodes: set[N] = set(graph.keys())
    for u in graph:
        nodes.update(graph[u].keys())

    indegree: dict[N, int] = {n: 0 for n in nodes}
    for u in graph:
        for v in graph[u]:
            indegree[v] = indegree.get(v, 0) + 1
    for n in nodes:
        indegree.setdefault(n, 0)

    queue: list[N] = [n for n in nodes if indegree[n] == 0]
    order: list[N] = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in graph.get(u, {}):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != len(nodes):
        raise ValueError("Graph contains a cycle; no topological order exists")
    return order


def kruskal_mst(num_nodes: int, edges: Iterable[tuple[N, N, float]]) -> list[tuple[N, N, float]]:
    """Minimum spanning tree via Kruskal's algorithm.

    Args:
        num_nodes: Total node count. Nodes are integers 0..num_nodes-1, or use
            ``UnionFind`` separately if using non-int labels (here we assume
            labels hashable and use UnionFind internally).
        edges: Iterable of ``(u, v, weight)``.

    Returns:
        List of edges ``(u, v, weight)`` that form the MST.

    Complexity:
        Time: O(E log E). Space: O(V + E).
    """
    # We collect node labels from edges to support arbitrary hashable nodes.
    edge_list = list(edges)
    nodes: set[N] = set()
    for u, v, _ in edge_list:
        nodes.add(u)
        nodes.add(v)
    uf = _UnionFindRaw(nodes)
    mst: list[tuple[N, N, float]] = []
    for u, v, w in sorted(edge_list, key=lambda e: e[2]):
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == len(nodes) - 1:
                break
    return mst


def prim_mst(graph: dict[N, dict[N, float]], start: N) -> list[tuple[N, N, float]]:
    """Minimum spanning tree via Prim's algorithm.

    Args:
        graph: Weighted undirected adjacency dict.
        start: Arbitrary starting node.

    Returns:
        List of edges ``(u, v, weight)`` in the MST.

    Complexity:
        Time: O(E log V). Space: O(V).
    """
    visited: set[N] = {start}
    edges: list[tuple[float, N, N]] = []
    for v, w in graph.get(start, {}).items():
        edges.append((w, start, v))
    heapq.heapify(edges)
    mst: list[tuple[N, N, float]] = []
    while edges and len(visited) < _count_nodes(graph):
        w, u, v = heapq.heappop(edges)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        for nxt, nw in graph.get(v, {}).items():
            if nxt not in visited:
                heapq.heappush(edges, (nw, v, nxt))
    return mst


def a_star(
    graph: dict[N, dict[N, float]],
    start: N,
    goal: N,
    heuristic: Callable[[N], float],
) -> list[N]:
    """A* shortest path search.

    Args:
        graph: Weighted adjacency dict.
        start: Source node.
        goal: Target node.
        heuristic: Callable ``h(node) -> non-negative float`` estimating
            distance to goal. Must be admissible for optimality.

    Returns:
        List of nodes forming the shortest path from ``start`` to ``goal``,
        inclusive. Empty list if no path exists.

    Complexity:
        Time: O(E log V) with a binary heap. Space: O(V).
    """
    if start == goal:
        return [start]
    open_heap: list[tuple[float, N]] = [(heuristic(start), start)]
    came_from: dict[N, N] = {}
    g_score: dict[N, float] = {start: 0}
    closed: set[N] = set()
    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        if current in closed:
            continue
        closed.add(current)
        for neighbor, weight in graph.get(current, {}).items():
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (tentative_g + heuristic(neighbor), neighbor))
    return []


# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #


class _UnionFindRaw:
    """Internal Union-Find for Kruskal; supports arbitrary hashable labels."""

    def __init__(self, elements: Iterable[N]) -> None:
        self.parent: dict[N, N] = {e: e for e in elements}
        self.rank: dict[N, int] = {e: 0 for e in self.parent}

    def find(self, x: N) -> N:
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a: N, b: N) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def _count_nodes(graph: dict[N, dict[N, float]]) -> int:
    nodes: set[N] = set(graph.keys())
    for u in graph:
        nodes.update(graph[u].keys())
    return len(nodes)


__all__ = [
    "bfs",
    "dfs",
    "dfs_recursive",
    "dijkstra",
    "bellman_ford",
    "floyd_warshall",
    "topological_sort",
    "kruskal_mst",
    "prim_mst",
    "a_star",
]