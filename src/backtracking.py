import time

def solve_backtracking(adj, k, params=None):
    n = len(adj)
    colors = [-1] * n
    nodes_explored = 0
    backtracks = 0

    def is_safe(node, color):
        for neigh in adj[node]:
            if colors[neigh] == color:
                return False
        return True

    def backtrack(node):
        nonlocal nodes_explored, backtracks

        if node == n:
            return True

        nodes_explored += 1

        for color in range(k):
            if is_safe(node, color):
                colors[node] = color
                if backtrack(node + 1):
                    return True
                colors[node] = -1  # undo
                backtracks += 1

        return False

    t0 = time.time()
    success = backtrack(0)
    t1 = time.time()

    if not success:
        return {
            "coloring": None,
            "nodes_explored": nodes_explored,
            "backtracks": backtracks,
            "time_ms": (t1 - t0) * 1000,
        }

    return {
        "coloring": {i: colors[i] for i in range(n)},
        "nodes_explored": nodes_explored,
        "backtracks": backtracks,
        "time_ms": (t1 - t0) * 1000,
    }
