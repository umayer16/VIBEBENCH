import heapq
from collections import defaultdict


def dijkstra(graph, start):
    """
    Dijkstra's algorithm to find shortest paths from start node to all other nodes.
    
    Args:
        graph: dict where keys are nodes, values are lists of (neighbor, weight) tuples
        start: starting node
        
    Returns:
        dict: node → shortest distance from start
    """
    # Initialize distances: infinity for all nodes except start (0)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Priority queue: (distance, node)
    pq = [(0, start)]  # heapq is min-heap
    
    # Keep track of visited nodes (optimization: we can skip already processed nodes)
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # If we already found a better path earlier, skip this one
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            if current_node in visited and neighbor in visited:
                continue
                
            distance = current_distance + weight
            
            # If we found a shorter path to neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Push the new better distance to the priority queue
                heapq.heappush(pq, (distance, neighbor))
    
    return distances


def print_shortest_paths(distances, start):
    """Pretty print the shortest distances from start node"""
    print(f"Shortest distances from node '{start}':")
    print("-" * 45)
    for node, dist in sorted(distances.items()):
        if dist == float('inf'):
            print(f"  → {node:>3} : unreachable")
        else:
            print(f"  → {node:>3} : {dist:>4}")
    print()


if __name__ == "__main__":
    # Sample weighted graph (adjacency list representation)
    # Format: {node: [(neighbor, weight), ...]}
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('D', 2)]
    }

    start_node = 'A'
    
    print("Graph structure:")
    for node, edges in graph.items():
        print(f"  {node} → {edges}")
    print()

    # Run Dijkstra
    shortest_distances = dijkstra(graph, start_node)
    
    # Output result
    print_shortest_paths(shortest_distances, start_node)

    # Bonus: another test case
    print("Another test case (starting from 'E'):")
    shortest_from_e = dijkstra(graph, 'E')
    print_shortest_paths(shortest_from_e, 'E')