import time


def solve_backtracking(adj, k, params=None):
    """
    Backtracking graph coloring with MRV + Forward Checking.

    :param adj: dict {node: [neighbors]}
    :param k:   maximum number of colors
    :param params: (unused for now, kept for consistency)
    :return: dict with keys:
             - "coloring": {node: color} or None if no solution
             - "nodes_explored": int
             - "backtracks": int
             - "time_ms": float (milliseconds)
    """

    n = len(adj)
    colors = [-1] * n  # -1 = uncolored

    # Domain for each node = all possible colors initially
    domains = {i: set(range(k)) for i in range(n)}

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
        Select the uncolored node with the smallest domain size (MRV).
        """
        uncolored = [i for i in range(n) if colors[i] == -1]
        if not uncolored:
            return None

        # MRV = choose node with minimum domain size
        return min(uncolored, key=lambda node: len(domains[node]))

    def forward_check(node, color):
        """
        Apply forward checking after assigning a color.
        Remove `color` from domains of neighbors.
        If any neighbor domain becomes empty -> failure.
        Return: removed_values (to allow undo)
        """
        removed = {}

        for neigh in adj[node]:
            if colors[neigh] == -1 and color in domains[neigh]:
                domains[neigh].remove(color)
                removed.setdefault(neigh, []).append(color)

                # No available colors → fail early
                if len(domains[neigh]) == 0:
                    return None  # failure

        return removed  # success

    def undo_forward_check(removed):
        """Restore pruned domain values."""
        for node, vals in removed.items():
            for v in vals:
                domains[node].add(v)

    def backtrack():
        nonlocal nodes_explored, backtracks

        # Base case: all nodes colored
        if all(colors[i] != -1 for i in range(n)):
            return True

        nodes_explored += 1

        # Select variable using MRV
        node = select_mrv_node()
        if node is None:
            return True  # should not really happen if base case above holds

        # Try colors in the node domain
        for color in list(domains[node]):
            if is_safe(node, color):
                colors[node] = color

                # Forward checking
                removed = forward_check(node, color)

                if removed is not None:
                    if backtrack():
                        return True

                # Undo assignment
                colors[node] = -1

                # Undo domain pruning
                if removed is not None:
                    undo_forward_check(removed)

                backtracks += 1

        return False

    # Run
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
