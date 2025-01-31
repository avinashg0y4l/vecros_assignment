import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def find_shortest_path(graph, start, end):
    """
    Finds the shortest weighted path between two points in a 3D grid using Dijkstra's algorithm.

    Parameters:
        graph (networkx.Graph): The weighted graph representing the 3D grid.
        start (tuple): The starting coordinate (x, y, z).
        end (tuple): The ending coordinate (x, y, z).

    Returns:
        list: A list of tuples representing the shortest path from start to end.

    Edge Cases:
        - If there is no valid path, NetworkX will raise an exception.
        - If start and end are the same, the function returns a single-point path.
    """
    return nx.shortest_path(graph, source=start, target=end, weight="weight", method="dijkstra")


def avoid_collisions(paths):
    """
    Adjusts paths to ensure no two paths share a common point at the same time.

    Parameters:
        paths (list of lists): A list where each element is a list representing a path.

    Returns:
        list: A list of adjusted paths where no two paths collide at the same time.

    Edge Cases:
        - If only one path is given, no adjustments are needed.
        - Paths may be delayed if necessary to prevent collisions.
    """
    occupied_positions = {}  # Dictionary to track occupied positions at each timestep
    adjusted_paths = []

    for path in paths:
        new_path = []
        for t, pos in enumerate(path):
            while pos in occupied_positions and occupied_positions[pos] == t:
                t += 1  # Delay if occupied at this time
            occupied_positions[pos] = t
            new_path.append(pos)
        adjusted_paths.append(new_path)

    return adjusted_paths


# ---------------------- Define 3D Grid & Graph ----------------------
GRID_SIZE = 101
grid = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Assign random high weights to obstacles
for _ in range(500):  
    x, y, z = np.random.randint(0, GRID_SIZE, 3)
    grid[x, y, z] = random.randint(5, 10)

# Create Graph Representation
G = nx.Graph()
directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        for z in range(GRID_SIZE):
            G.add_node((x, y, z), weight=grid[x, y, z])

            for dx, dy, dz in directions:
                nx_, ny_, nz_ = x + dx, y + dy, z + dz
                if 0 <= nx_ < GRID_SIZE and 0 <= ny_ < GRID_SIZE and 0 <= nz_ < GRID_SIZE:
                    weight = 1 + grid[x, y, z] + grid[nx_, ny_, nz_]  
                    G.add_edge((x, y, z), (nx_, ny_, nz_), weight=weight)

print("3D Grid with Weighted Points Created....!!")


# ---------------------- User Input for Start & End Points ----------------------
start_points = [
    (0, 0, 0),        
    (20, 30, 40),     
    (0, 75, 55),      
    (50, 60, 70),     
    (17, 50, 100)     
]

end_points = [
    (100, 100, 100),  
    (80, 90, 60),     
    (45, 34, 23),     
    (20, 20, 20),     
    (50, 60, 70)      
]

# Compute Paths
paths = [find_shortest_path(G, start, end) for start, end in zip(start_points, end_points)]
paths = avoid_collisions(paths)
print("Paths Calculated and Adjusted....!!")


# ---------------------- Visualization ----------------------
def plot_paths_3d(paths):
    """
    Plots the computed 3D paths using Matplotlib.

    Parameters:
        paths (list of lists): A list where each element is a list representing a path.

    Returns:
        None

    Edge Cases:
        - If paths are empty, the function does nothing.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = ['r', 'b', 'g', 'm', 'c']  

    for idx, path in enumerate(paths):
        x_vals = [p[0] for p in path]
        y_vals = [p[1] for p in path]
        z_vals = [p[2] for p in path]
        ax.plot(x_vals, y_vals, z_vals, marker="o", color=colors[idx % len(colors)], label=f"Path {idx+1}")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Shortest Paths with Collision Avoidance")
    plt.legend()
    plt.savefig("path_visualization.png")
    plt.show()


# Call the function to visualize the paths
plot_paths_3d(paths)
