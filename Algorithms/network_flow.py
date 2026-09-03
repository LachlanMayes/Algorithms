"""Network flow algorithms and matching.

Reference: arXiv:2401.05627 - "Deterministic Near-Linear Time Minimum Cut
in Weighted Graphs" (Henzinger, Li, Rao, Wang) - related to flow-based
methods.

Implements:
    - Ford-Fulkerson / Edmonds-Karp maximum flow.
    - Minimum s-t cut (min-cut / max-flow theorem).
    - Hopcroft-Karp maximum bipartite matching.
"""

from __future__ import annotations

from collections import deque
from typing import Hashable, TypeVar

N = TypeVar("N", bound=Hashable)


def ford_fulkerson(
    graph: dict[N, dict[N, float]], source: N, sink: N
) -> float:
    """Maximum flow via Ford-Fulkerson with BFS augmenting paths
    (i.e. Edmonds-Karp). Graph may have both forward and reverse edges;
    we add residual edges automatically.

    Args:
        graph: Adjacency dict ``{u: {v: capacity}}``.
        source: Source node.
        sink: Sink node.

    Returns:
        Maximum flow value from ``source`` to ``sink``.

    Complexity:
        Time: O(V * E^2) for Edmonds-Karp; O(E * max_flow) for plain FF.
        Space: O(V + E).
    """
    residual: dict[N, dict[N, float]] = {
        u: dict(neighbors) for u, neighbors in graph.items()
    }
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
    for u in list(residual):
        for v in list(residual[u]):
            if u not in residual[v]:
                residual[v][u] = 0.0

    max_flow = 0.0
    while True:
        parent: dict[N, N | None] = {source: None}
        q = deque([source])
        found = False
        while q and not found:
            u = q.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in parent and cap > 0:
                    parent[v] = u
                    if v == sink:
                        found = True
                        break
                    q.append(v)
        if not found:
            break

        bottleneck = float("inf")
        v = sink
        while v != source:
            u = parent[v]  # type: ignore[assignment]
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        if bottleneck == float("inf"):
            break

        v = sink
        while v != source:
            u = parent[v]  # type: ignore[assignment]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u
        max_flow += bottleneck
    return max_flow


def edmonds_karp(
    graph: dict[N, dict[N, float]], source: N, sink: N
) -> float:
    """Alias for :func:`ford_fulkerson` (which uses BFS augmenting paths).

    Complexity: O(V * E^2).
    """
    return ford_fulkerson(graph, source, sink)


def min_cut(
    graph: dict[N, dict[N, float]], source: N, sink: N
) -> tuple[float, set[N]]:
    """Min s-t cut: minimum total capacity whose removal disconnects ``sink``
    from ``source``. Found as the min cut dual to max flow.

    Args:
        graph: Capacity dict.
        source: Source node.
        sink: Sink node.

    Returns:
        ``(cut_value, reachable_from_source)`` where ``reachable_from_source``
        is the set of nodes still reachable from ``source`` in the residual
        graph. Cut edges are those from reachable to non-reachable.

    Complexity:
        Time: O(V * E^2).
    """
    residual: dict[N, dict[N, float]] = {
        u: dict(neighbors) for u, neighbors in graph.items()
    }
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
    for u in list(residual):
        for v in list(residual[u]):
            if u not in residual[v]:
                residual[v][u] = 0.0

    while True:
        parent: dict[N, N | None] = {source: None}
        q = deque([source])
        found = False
        while q and not found:
            u = q.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in parent and cap > 0:
                    parent[v] = u
                    if v == sink:
                        found = True
                        break
                    q.append(v)
        if not found:
            break
        bottleneck = float("inf")
        v = sink
        while v != source:
            u = parent[v]  # type: ignore[assignment]
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        if bottleneck == float("inf"):
            break
        v = sink
        while v != source:
            u = parent[v]  # type: ignore[assignment]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u

    reachable: set[N] = set()
    q = deque([source])
    reachable.add(source)
    while q:
        u = q.popleft()
        for v, cap in residual.get(u, {}).items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                q.append(v)
    cut_value = 0.0
    for u in reachable:
        for v, cap in graph.get(u, {}).items():
            if v not in reachable:
                cut_value += cap
    return cut_value, reachable


# --------------------------------------------------------------------------- #
# Hopcroft-Karp maximum bipartite matching
# --------------------------------------------------------------------------- #


def hopcroft_karp(
    graph: dict[N, list[N]], left_nodes: list[N], right_nodes: list[N]
) -> tuple[dict[N, N], dict[N, N]]:
    """Maximum bipartite matching via Hopcroft-Karp (1973).

    Args:
        graph: Adjacency list ``{left_node: [right_node, ...]}``.
        left_nodes: All left-side nodes.
        right_nodes: All right-side nodes (currently used to initialise
            the right_match dict, though unmatched right nodes simply have
            no entry).

    Returns:
        ``(left_match, right_match)`` where ``left_match[u]`` is the right
        node matched to left node ``u`` (or absent) and similarly for the
        other side.

    Complexity:
        Time: O(E * sqrt(V)). Space: O(V + E).
    """
    left_match: dict[N, N] = {}
    right_match: dict[N, N] = {}
    dist: dict[N, int] = {}

    def bfs() -> bool:
        """Build layered graph. Returns True iff there is a free right node
        reachable via alternating paths from some free left node."""
        for u in left_nodes:
            if u not in left_match:
                dist[u] = 0
            else:
                dist[u] = -1
        q = deque([u for u in left_nodes if u not in left_match])
        found = False
        while q:
            u = q.popleft()
            for v in graph.get(u, []):
                partner = right_match.get(v)
                if partner is None:
                    found = True
                elif dist.get(partner, -1) == -1:
                    dist[partner] = dist[u] + 1
                    q.append(partner)
        return found

    def dfs(u: N) -> bool:
        """DFS along layered graph to find augmenting path."""
        for v in graph.get(u, []):
            partner = right_match.get(v)
            if partner is None or (
                dist.get(partner, -1) == dist[u] + 1 and dfs(partner)
            ):
                left_match[u] = v
                right_match[v] = u
                return True
        dist[u] = -1
        return False

    while bfs():
        for u in left_nodes:
            if u not in left_match:
                dfs(u)
    return left_match, right_match


__all__ = ["ford_fulkerson", "edmonds_karp", "min_cut", "hopcroft_karp"]