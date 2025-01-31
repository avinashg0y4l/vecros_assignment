# 3D Path Planning Assignment
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------------- 1️⃣ Function Definitions ----------------------

def find_shortest_path(graph, start, end):
    """Finds the shortest weighted path between two points using Dijkstra's algorithm."""
    return nx.shortest_path(graph, source=start, target=end, weight="weight", method="dijkstra")

def avoid_collisions(paths):
    """Ensures no two paths share a common point at the same time."""
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

# ---------------------- 2️⃣ Define Grid & Graph ----------------------
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

# ---------------------- 3️⃣ User Input for Start & End Points ----------------------
start_points =  [(0, 0, 0), (20, 30, 40), (0, 75, 55)]
end_points =    [(100, 100, 100), (80, 90, 60), (45, 34, 23)]

# Compute Paths
paths = [find_shortest_path(G, start, end) for start, end in zip(start_points, end_points)]
paths = avoid_collisions(paths)
print("Paths Calculated and Adjusted....!!")

# ---------------------- 4️⃣ Visualization ----------------------
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
