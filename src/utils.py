
import random

def generate_random_graph(n, p):
    """
    -Creates a random undirected graph with n nodes.
    -Each edge exists with probability p.
    -Returns an adjacency list: adj[node] = list of neighbors.
    """
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                adj[i].append(j)
                adj[j].append(i)
    return adj


def check_coloring(adj, coloring):
    """
    -Checks if a coloring is valid.
    -Returns (is_valid, number_of_conflicts).
    -A conflict is when two connected nodes have the same color.
    """
    if coloring is None:
        return (False, None)

    conflicts = 0
    for u in adj:
        for v in adj[u]:
            if u < v:  
                if coloring.get(u) == coloring.get(v):
                    conflicts += 1
    return (conflicts == 0, conflicts)


def count_colors(coloring):
    """
    -Counts how many distinct colors appear in the coloring.
    """
    if coloring is None:
        return 0
    return len(set(coloring.values()))
