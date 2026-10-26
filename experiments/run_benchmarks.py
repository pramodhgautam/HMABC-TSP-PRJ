import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from tsp_loader import load_instance_from_tsplib
from hmabc import HMABC
from visualizer import plot_tour, plot_convergence

def run_experiment(instance_name, runs=10):
    print(f"--- Running HMABC on {instance_name.upper()} ({runs} runs) ---")
    dim, nodes, dist_matrix, optimal = load_instance_from_tsplib(instance_name)
    
    if dist_matrix is None:
        print("Failed to load instance.")
        return

    results = []
    best_overall_tour = None
    best_overall_length = float('inf')
    best_history = []

    for run in range(runs):
        print(f"Run {run + 1}/{runs}...", end="\r")
        # Parameters tuned for standard benchmarks
        abc = HMABC(dist_matrix, num_bees=40, max_cycles=500, limit=50)
        tour, length, history = abc.run()
        results.append(length)
        
        if length < best_overall_length:
            best_overall_length = length
            best_overall_tour = tour
            best_history = history

    print(f"\nCompleted {runs} runs.")
    print(f"Optimal (Known): {optimal}")
    print(f"Best Found:      {best_overall_length:.2f}")
    print(f"Mean:            {np.mean(results):.2f} ± {np.std(results):.2f}")
    
    # Calculate gap if optimal is known
    if optimal:
        gap = ((best_overall_length - optimal) / optimal) * 100
        print(f"Optimality Gap:  {gap:.2f}%")

    # Save visualizations for the best run
    os.makedirs("results", exist_ok=True)
    plot_tour(nodes, best_overall_tour, instance_name, title=f"Best Tour (Length: {best_overall_length:.2f})")
    plot_convergence(best_history, instance_name, title=f"HMABC Convergence")    
    print("Visualizations saved to /results/")

if __name__ == "__main__":
    # Standard TSPLIB instances (offline-capable)
    instances = ["eil51", "berlin52"]
    for inst in instances:
        run_experiment(inst, runs=10) # Change to 30 for full statistical rigor