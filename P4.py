# ==========================================
# PROBLEM 4: MULTI-OBJECTIVE ROUTING (DIJKSTRA)
# ==========================================
import heapq

def find_routes(graph_map, start, end):
    # Queue stores: (distance, toll, current_node, path)
    queue = [(0, graph_map[start]["toll"], start, [start])]
    
    # Track Pareto frontier per node: list of (distance, toll)
    # A path is valid if no other path to this node is strictly better in both metrics.
    pareto_fronts = {node:[] for node in graph_map}
    valid_routes_to_end =[]

    while queue:
        dist, toll, node, path = heapq.heappop(queue)

        # Check if dominated at current node
        is_dominated = False
        for d, t in pareto_fronts[node]:
            if d <= dist and t <= toll:
                is_dominated = True
                break
        
        if is_dominated:
            continue
            
        pareto_fronts[node].append((dist, toll))

        if node == end:
            valid_routes_to_end.append({"path": path, "dist": dist, "toll": toll})
            continue

        for neighbor, edge_dist in graph_map[node]["roads"].items():
            new_dist = dist + edge_dist
            new_toll = toll + graph_map[neighbor]["toll"]
            heapq.heappush(queue, (new_dist, new_toll, neighbor, path + [neighbor]))

    # Filter final routes to ensure strictly inefficient routes are removed
    final_routes =[]
    for r1 in valid_routes_to_end:
        dominated = False
        for r2 in valid_routes_to_end:
            if r1 != r2 and r2["dist"] <= r1["dist"] and r2["toll"] <= r1["toll"]:
                dominated = True
                break
        if not dominated:
            final_routes.append(r1)

    return final_routes

# Example Execution:
graph_map = {
    "A": {"toll": 0, "roads": {"B": 4, "C": 8}},
    "B": {"toll": 2, "roads": {"A": 4, "C": 2, "D": 5}},
    "C": {"toll": 3, "roads": {"A": 8, "B": 2, "D": 3, "E": 6}},
    "D": {"toll": 2, "roads": {"B": 5, "C": 3, "E": 2}},
    "E": {"toll": 5, "roads": {"C": 6, "D": 2}},
}

# routes = find_routes(graph_map, "A", "E")
# print("Available Efficient Routes:", routes)