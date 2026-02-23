import heapq


def dijkstra(graph, start):
    """
    Computes the shortest distances from the start node to all other nodes
    in a weighted graph using Dijkstra's algorithm.

    :param graph: Dict representing adjacency list
                  {node: [(neighbor, weight), ...]}
    :param start: The starting node
    :return: Dict of shortest distances from start to each node
    """
    # Initialize distances with infinity
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    # Priority queue to store (distance, node)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if we found a better path already
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # If a shorter path to neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


if __name__ == "__main__":
    # Sample graph with at least 4 nodes (adjacency list)
    # Graph structure:
    # A --1--> B
    # A --4--> C
    # B --2--> C
    # B --5--> D
    # C --1--> D
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": []
    }

    start_node = "A"
    shortest_distances = dijkstra(graph, start_node)

    print(f"Shortest distances from node '{start_node}':")
    for node, distance in shortest_distances.items():
        print(f"{start_node} -> {node}: {distance}")