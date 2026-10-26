import tsplib95
import numpy as np

def load_tsp_instance(instance_name: str):
    """
    Loads a TSPLIB instance and returns the problem, optimal value, and distance matrix.
    """
    problem = tsplib95.load_problem(f"../data/{instance_name}.tsp") # Assumes data folder, or we can load from URL
    # Alternatively, load directly from tsplib95 standard problems if available, 
    # but for simplicity, we'll compute distance matrix from nodes.
    
    # For standard instances, tsplib95 can load them by name if we use a known path or URL.
    # Let's use a robust method: download or use built-in if available. 
    # Actually, tsplib95 has a standard way to load by name if we point to a URL or local file.
    # We will write a helper to fetch standard instances.
    pass

def get_distance_matrix(nodes):
    """Computes Euclidean distance matrix for a list of (x, y) nodes."""
    n = len(nodes)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(np.array(nodes[i]) - np.array(nodes[j]))
            dist_matrix[i, j] = dist
            dist_matrix[j, i] = dist
    return dist_matrix

def load_instance_from_tsplib(instance_name):
    """Fetches standard TSPLIB instances dynamically."""
    import urllib.request
    url = f"http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/{instance_name}.tsp"
    try:
        response = urllib.request.urlopen(url)
        problem = tsplib95.parse(response.read().decode('utf-8'))
        nodes = [problem.get_display(i+1) for i in range(problem.dimension)]
        dist_matrix = get_distance_matrix(nodes)
        optimal = problem.optimal if hasattr(problem, 'optimal') and problem.optimal else None
        return problem.dimension, nodes, dist_matrix, optimal
    except Exception as e:
        print(f"Error loading {instance_name}: {e}")
        return None, None, None, None
