
import time
import csv
import os
from src.utils import generate_random_graph, check_coloring, count_colors

# Try importing algorithms (they may not exist yet)
try:
    from src.backtracking import solve_backtracking
except:
    solve_backtracking = None

try:
    from src.cultural import solve_cultural
except:
    solve_cultural = None


def run_one_test(adj, k):
    """
    Runs both algorithms on the same graph.
    Returns rows ready to write to CSV.
    """
    rows = []

    # Backtracking
    if solve_backtracking is not None:
        start = time.perf_counter()
        result = solve_backtracking(adj, k)
        elapsed = (time.perf_counter() - start) * 1000
        coloring = result["coloring"]
        is_valid, conflicts = check_coloring(adj, coloring)
        rows.append(("backtracking", count_colors(coloring), conflicts, elapsed))
    else:
        rows.append(("backtracking", None, None, None))

    # Cultural Algorithm
    if solve_cultural is not None:
        start = time.perf_counter()
        result = solve_cultural(adj, k)
        elapsed = (time.perf_counter() - start) * 1000
        coloring = result["coloring"]
        is_valid, conflicts = check_coloring(adj, coloring)
        rows.append(("cultural", count_colors(coloring), conflicts, elapsed))
    else:
        rows.append(("cultural", None, None, None))

    return rows


def main():
    os.makedirs("results", exist_ok=True)
    out_path = "results/summary.csv"

    sizes = [10, 20, 40]   # small sizes to test
    p = 0.2
    k = 3

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "algorithm", "colors", "conflicts", "time_ms"])

        for n in sizes:
            adj = generate_random_graph(n, p)
            rows = run_one_test(adj, k)

            for (alg, colors, conflicts, ms) in rows:
                writer.writerow([n, alg, colors, conflicts, ms])

    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
