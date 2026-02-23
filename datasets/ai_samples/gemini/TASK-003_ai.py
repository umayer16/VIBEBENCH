import heapq

def dijkstra(graph, start_node):
    """
    Finds the shortest distance from a start_node to all other nodes in a weighted graph.
    
    Args:
        graph (dict): Adjacency list where graph[u] = [(v, weight), ...]
        start_node: The node to start the search from.
        
    Returns:
        dict: A dictionary mapping each node to its shortest distance from start_node.
    """
    # Initialize distances with infinity, start_node with 0
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    
    # Priority queue stores tuples: (distance, node)
    # We use distance first so the heap stays sorted by the smallest distance
    priority_queue = [(0, start_node)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If we found a longer path already processed, skip it
        if current_distance > distances[current_node]:
            continue
            
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return distances

if __name__ == "__main__":
    # Sample Graph represented as an Adjacency List
    # Nodes: A, B, C, D, E
    sample_graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 5), ('D', 10)],
        'C': [('D', 3)],
        'D': [('E', 7)],
        'E': []
    }
    
    start = 'A'
    print(f"Calculating shortest paths from node: {start}")
    
    shortest_distances = dijkstra(sample_graph, start)
    
    print("\nNode | Distance from " + start)
    print("-" * 25)
    for node, dist in sorted(shortest_distances.items()):
        print(f"{node:4} | {dist}")