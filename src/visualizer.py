import matplotlib.pyplot as plt
import numpy as np
import os

def plot_tour(nodes, tour, instance_name, title="Best Tour Found"):
    """Plots the TSP cities and the optimal route."""
    fig, ax = plt.subplots(figsize=(8, 8))
    x = [node[0] for node in nodes]
    y = [node[1] for node in nodes]
    
    # Plot cities
    ax.scatter(x, y, c='red', s=15, zorder=2)
    for i, (xi, yi) in enumerate(zip(x, y)):
        ax.annotate(str(i+1), (xi, yi), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)
    
    # Plot tour
    tour_x = [x[i] for i in tour] + [x[tour[0]]]
    tour_y = [y[i] for i in tour] + [y[tour[0]]]
    ax.plot(tour_x, tour_y, 'b-', linewidth=1, zorder=1)
    
    ax.set_title(f"{title} ({instance_name.upper()})")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Save with unique name
    os.makedirs("results", exist_ok=True)
    plt.savefig(f"results/{instance_name}_tour.png", dpi=300)
    plt.close()

def plot_convergence(history, instance_name, title="HMABC Convergence Curve"):
    """Plots the convergence history of the algorithm."""
    plt.figure(figsize=(8, 5))
    plt.plot(history, color='#1F3864', linewidth=2)
    plt.title(f"{title} ({instance_name.upper()})")
    plt.xlabel("Iteration (Cycle)")
    plt.ylabel("Best Tour Length")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Save with unique name
    os.makedirs("results", exist_ok=True)
    plt.savefig(f"results/{instance_name}_convergence.png", dpi=300)
    plt.close()