import heapq
from collections import defaultdict
import math


class Graph:
    """A weighted graph implementation using adjacency list."""
    
    def __init__(self):
        """Initialize an empty graph."""
        self.adjacency_list = defaultdict(list)
        self.nodes = set()
    
    def add_edge(self, from_node, to_node, weight):
        """
        Add a weighted edge to the graph.
        
        Args:
            from_node: Source node
            to_node: Destination node
            weight: Weight of the edge (must be non-negative for Dijkstra)
        """
        if weight < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative weights")
        
        self.adjacency_list[from_node].append((to_node, weight))
        self.nodes.add(from_node)
        self.nodes.add(to_node)
    
    def add_undirected_edge(self, node1, node2, weight):
        """Add an undirected weighted edge (adds edges in both directions)."""
        self.add_edge(node1, node2, weight)
        self.add_edge(node2, node1, weight)


def dijkstra_shortest_path(graph, start_node):
    """
    Find shortest paths from start_node to all other nodes using Dijkstra's algorithm.
    
    Args:
        graph: Graph object with adjacency_list attribute
        start_node: The starting node for path finding
        
    Returns:
        tuple: (distances, predecessors)
            - distances: Dictionary mapping node -> shortest distance from start
            - predecessors: Dictionary mapping node -> previous node in shortest path
    """
    # Initialize distances with infinity for all nodes
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    
    # Keep track of predecessors to reconstruct paths
    predecessors = {node: None for node in graph.nodes}
    
    # Priority queue: (distance, node)
    priority_queue = [(0, start_node)]
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip if we've already processed this node with a shorter distance
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Check all neighbors of current node
        for neighbor, weight in graph.adjacency_list[current_node]:
            distance = current_distance + weight
            
            # If we found a shorter path to the neighbor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, predecessors


def reconstruct_path(predecessors, start_node, end_node):
    """
    Reconstruct the shortest path from start_node to end_node.
    
    Args:
        predecessors: Dictionary mapping node -> previous node in shortest path
        start_node: Starting node
        end_node: Destination node
        
    Returns:
        list: Path from start_node to end_node (or empty list if no path exists)
    """
    path = []
    current = end_node
    
    # If there's no path to end_node
    if predecessors.get(end_node) is None and end_node != start_node:
        return []
    
    # Reconstruct path backwards
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    # Reverse to get path from start to end
    return list(reversed(path))


def print_shortest_paths(graph, start_node, distances, predecessors):
    """
    Print shortest paths from start_node to all other nodes.
    
    Args:
        graph: Graph object
        start_node: Starting node
        distances: Dictionary of shortest distances
        predecessors: Dictionary of predecessors
    """
    print(f"Shortest paths from node '{start_node}':")
    print("=" * 50)
    
    for node in sorted(graph.nodes):
        if node == start_node:
            continue
            
        distance = distances[node]
        
        if distance == float('inf'):
            print(f"To {node}: No path exists")
        else:
            path = reconstruct_path(predecessors, start_node, node)
            path_str = " → ".join(str(p) for p in path)
            print(f"To {node}: Distance = {distance}, Path: {path_str}")
    
    print()


if __name__ == "__main__":
    # Create a sample graph with at least 4 nodes
    print("Dijkstra's Algorithm - Shortest Path Finder")
    print("=" * 60)
    
    # Example 1: Simple directed graph
    print("Example 1: Directed Graph")
    print("-" * 40)
    
    graph1 = Graph()
    # Add edges: (from, to, weight)
    graph1.add_edge('A', 'B', 4)
    graph1.add_edge('A', 'C', 2)
    graph1.add_edge('B', 'C', 1)
    graph1.add_edge('B', 'D', 5)
    graph1.add_edge('C', 'D', 8)
    graph1.add_edge('C', 'E', 10)
    graph1.add_edge('D', 'E', 2)
    graph1.add_edge('D', 'F', 6)
    graph1.add_edge('E', 'F', 3)
    
    # Run Dijkstra from node 'A'
    distances, predecessors = dijkstra_shortest_path(graph1, 'A')
    print_shortest_paths(graph1, 'A', distances, predecessors)
    
    # Example 2: Undirected graph (city distances)
    print("\nExample 2: Undirected Graph (City Distances)")
    print("-" * 40)
    
    graph2 = Graph()
    # Add undirected edges (roads between cities)
    graph2.add_undirected_edge('New York', 'Boston', 215)
    graph2.add_undirected_edge('New York', 'Philadelphia', 95)
    graph2.add_undirected_edge('New York', 'Washington DC', 225)
    graph2.add_undirected_edge('Boston', 'Philadelphia', 310)
    graph2.add_undirected_edge('Philadelphia', 'Washington DC', 140)
    graph2.add_undirected_edge('Washington DC', 'Richmond', 110)
    graph2.add_undirected_edge('Philadelphia', 'Richmond', 245)
    
    # Run Dijkstra from 'New York'
    distances2, predecessors2 = dijkstra_shortest_path(graph2, 'New York')
    print_shortest_paths(graph2, 'New York', distances2, predecessors2)
    
    # Example 3: Graph with unreachable nodes
    print("\nExample 3: Graph with Unreachable Nodes")
    print("-" * 40)
    
    graph3 = Graph()
    graph3.add_edge(1, 2, 3)
    graph3.add_edge(2, 3, 4)
    graph3.add_edge(4, 5, 2)  # This component is disconnected from node 1
    
    distances3, predecessors3 = dijkstra_shortest_path(graph3, 1)
    print_shortest_paths(graph3, 1, distances3, predecessors3)
    
    # Demonstrate path reconstruction for a specific destination
    print("\nDetailed Path Reconstruction:")
    print("-" * 40)
    
    start = 'A'
    destination = 'F'
    path = reconstruct_path(predecessors, start, destination)
    
    if path:
        print(f"Shortest path from {start} to {destination}: {' → '.join(path)}")
        print(f"Total distance: {distances[destination]}")
    else:
        print(f"No path exists from {start} to {destination}")
    
    # Verify algorithm properties
    print("\n" + "=" * 60)
    print("Algorithm Properties:")
    print("- Works with non-negative weights only")
    print(f"- Time complexity: O((V + E) log V) with binary heap")
    print(f"- Space complexity: O(V)")