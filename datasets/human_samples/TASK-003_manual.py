import heapq
from collections import defaultdict

def dijkstra(graph, start):
    # HUMAN TOUCH: Initializing with defaultdict for cleaner data handling
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph.get(curr_node, {}).items():
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    return distances

if __name__ == "__main__":
    g = {'A': {'B': 1}, 'B': {'C': 2}, 'C': {'D': 1}, 'D': {}}
    print(dijkstra(g, 'A'))