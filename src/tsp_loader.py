import numpy as np

# Hardcoded standard TSPLIB instances for 100% reproducible, offline execution.
# This ensures the benchmark runs flawlessly without external network dependencies.
TSPLIB_INSTANCES = {
    "eil51": {
        "optimal": 426,
        "nodes": [
            (37, 52), (49, 49), (52, 64), (20, 26), (40, 30), (21, 47), (17, 63),
            (31, 62), (52, 33), (51, 21), (42, 41), (31, 32), (5, 25), (12, 42),
            (36, 16), (52, 41), (27, 23), (17, 33), (13, 13), (57, 58), (62, 42),
            (42, 57), (16, 57), (8, 52), (7, 38), (27, 68), (30, 48), (43, 67),
            (58, 48), (58, 27), (37, 69), (38, 46), (46, 10), (61, 33), (62, 63),
            (63, 69), (32, 22), (45, 35), (59, 15), (5, 6), (10, 17), (21, 10),
            (5, 64), (30, 15), (39, 10), (32, 39), (25, 32), (25, 55), (48, 28),
            (56, 37), (30, 40)
        ]
    },
    "berlin52": {
        "optimal": 7542,
        "nodes": [
            (565, 575), (25, 185), (345, 750), (945, 685), (845, 655), (880, 660),
            (25, 230), (525, 1000), (580, 1175), (650, 1130), (1605, 620), (1220, 580),
            (1465, 200), (1530, 5), (845, 680), (725, 370), (145, 665), (415, 635),
            (510, 875), (560, 365), (300, 465), (520, 585), (480, 415), (835, 625),
            (975, 580), (1215, 245), (1320, 315), (1250, 400), (660, 180), (410, 250),
            (420, 555), (575, 665), (1150, 1160), (700, 580), (685, 595), (685, 610),
            (770, 610), (795, 645), (720, 635), (760, 650), (475, 960), (95, 260),
            (875, 920), (700, 500), (555, 815), (830, 485), (1170, 65), (830, 610),
            (605, 625), (595, 360), (1340, 725), (1740, 245)
        ]
    }
}

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
    """Loads a standard TSPLIB instance from the hardcoded dictionary."""
    instance_name = instance_name.lower()
    if instance_name not in TSPLIB_INSTANCES:
        print(f"Instance {instance_name} not found in local database.")
        return None, None, None, None
    
    data = TSPLIB_INSTANCES[instance_name]
    nodes = data["nodes"]
    optimal = data["optimal"]
    dist_matrix = get_distance_matrix(nodes)
    
    return len(nodes), nodes, dist_matrix, optimal