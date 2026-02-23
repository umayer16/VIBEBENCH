import heapq


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path if path[0] == start else []


def print_results(distances, previous, start):
    print(f"\nShortest distances from node '{start}':\n")
    print(f"  {'Node':<10} {'Distance':<12} {'Path'}")
    print(f"  {'-'*40}")
    for node in sorted(distances):
        dist = distances[node]
        path = reconstruct_path(previous, start, node)
        path_str = " -> ".join(path) if path else "unreachable"
        dist_str = str(dist) if dist != float('inf') else "∞"
        print(f"  {node:<10} {dist_str:<12} {path_str}")


if __name__ == "__main__":
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 6},
        'C': {'A': 4, 'B': 2, 'D': 3, 'E': 5},
        'D': {'B': 6, 'C': 3, 'E': 1},
        'E': {'C': 5, 'D': 1},
    }

    print("Graph (adjacency list):")
    for node, neighbors in graph.items():
        edges = ", ".join(f"{nb}(w={w})" for nb, w in neighbors.items())
        print(f"  {node} -> {edges}")

    start_node = 'A'
    distances, previous = dijkstra(graph, start_node)
    print_results(distances, previous, start_node)