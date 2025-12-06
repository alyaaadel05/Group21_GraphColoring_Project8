import time


def solve_backtracking(adj, k, params=None):
    """
    Backtracking graph coloring with MRV (Minimum Remaining Values) heuristic.

    adj : dict[int, list[int]]
        Adjacency list for graph, nodes are 0 .. n-1
    k   : int
        Maximum number of colors allowed (0 .. k-1)

    Returns a dictionary:
        {
            "coloring": {node: color} or None if no solution,
            "nodes_explored": int,
            "backtracks": int,
            "time_ms": float
        }
    """
    n = len(adj)
    colors = [-1] * n  # -1 = uncolored

    nodes_explored = 0
    backtracks = 0

    def is_safe(node, color):
        """Check if we can assign this color to this node."""
        for neigh in adj[node]:
            if colors[neigh] == color:
                return False
        return True

    def select_mrv_node():
        """
        Select the next node to color using MRV:
        choose the uncolored node with the fewest legal colors.
        """
        best_node = None
        best_count = None

        for node in range(n):
            if colors[node] != -1:
                continue  # already colored

            # count legal colors for this node
            legal_count = 0
            for c in range(k):
                if is_safe(node, c):
                    legal_count += 1

            # if no legal colors -> immediate failure
            if legal_count == 0:
                return node, 0

            if best_count is None or legal_count < best_count:
                best_count = legal_count
                best_node = node

        return best_node, best_count

    def all_colored():
        return all(c != -1 for c in colors)

    def backtrack():
        nonlocal nodes_explored, backtracks

        # Base case
        if all_colored():
            return True

        nodes_explored += 1

        # Choose next variable with MRV
        node, legal_count = select_mrv_node()

        # If no legal colors for this node → dead end
        if legal_count == 0:
            backtracks += 1
            return False

        # Try all legal colors for that node
        for color in range(k):
            if is_safe(node, color):
                colors[node] = color
                if backtrack():
                    return True
                # undo assignment
                colors[node] = -1
                backtracks += 1

        return False

    t0 = time.time()
    success = backtrack()
    t1 = time.time()

    result = {
        "coloring": None,
        "nodes_explored": nodes_explored,
        "backtracks": backtracks,
        "time_ms": (t1 - t0) * 1000,
    }

    if success:
        result["coloring"] = {i: colors[i] for i in range(n)}

    return result
