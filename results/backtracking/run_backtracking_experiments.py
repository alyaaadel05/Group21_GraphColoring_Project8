import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT)

import csv
import time

from src.utils import generate_random_graph
from src.backtracking import solve_backtracking


# 1. Define experiment settings

GRAPH_SIZES = [10, 20, 30]       # You can add: 40, 50, 60 if you want
EDGE_PROBABILITIES = [0.2, 0.4]  # Sparse vs dense
K_VALUES = [3]                   # Number of colors allowed

HEURISTIC_SETTINGS = [
    {"name": "MRV", "params": {}},
    {"name": "MRV+DH", "params": {"use_degree_heuristic": True}},
    {"name": "MRV+LCV", "params": {"use_lcv": True}},
    {"name": "MRV+DH+LCV", "params": {"use_degree_heuristic": True, "use_lcv": True}},
]



# 2. Run one experiment

def run_single_experiment(n, p, k, setting):
    params = setting["params"]
    name = setting["name"]

    adj = generate_random_graph(n, p)

    start = time.time()
    result = solve_backtracking(adj, k, params)
    end = time.time()

    return {
        "n": n,
        "p": p,
        "k": k,
        "heuristic": name,
        "nodes_explored": result["nodes_explored"],
        "backtracks": result["backtracks"],
        "time_ms": (end - start) * 1000
    }



# 3. Main experiment loop

def main():
    # Ensure results folder exists
    output_folder = "results/backtracking"
    os.makedirs(output_folder, exist_ok=True)

    output_csv = os.path.join(output_folder, "backtracking_results.csv")

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "n", "p", "k", "heuristic",
            "nodes_explored", "backtracks", "time_ms"
        ])

        # Run experiments
        for n in GRAPH_SIZES:
            for p in EDGE_PROBABILITIES:
                for k in K_VALUES:
                    for setting in HEURISTIC_SETTINGS:
                        print(f"Running n={n}, p={p}, k={k}, heuristic={setting['name']}")

                        result = run_single_experiment(n, p, k, setting)

                        writer.writerow([
                            result["n"],
                            result["p"],
                            result["k"],
                            setting["name"],
                            result["nodes_explored"],
                            result["backtracks"],
                            result["time_ms"]
                        ])

    print(f"\n✔ Experiments complete! Results saved to:\n{output_csv}")


if __name__ == "__main__":
    main()
