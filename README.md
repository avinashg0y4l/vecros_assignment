# **Vecros Robotics Assignment - Drone Mission & Path Planning**

## **Project Overview**
This repository contains two primary scripts for solving the given problem statement:

<<<<<<< HEAD
1. **Path Planning (`path_Planning.py`)**  
   - Implements **3D path planning** ensuring multiple paths do not coincide.  
   - Visualizes the planned paths.  
=======
This project implements **Path Planning** with collision avoidance and **Drone Navigation** . The goal is to plan a drone's flight path using predefined waypoints and simulate its journey, while ensuring safety by avoiding collisions.
>>>>>>> 4624a3e2f3b7bc8f789ad6cf552fe039419dbede

2. **Drone Mission (`Drone_Simulation.py`)**  
   - Plans and executes a **quadcopter mission in AUTO mode** using DroneKit.  
   - Includes real-time telemetry updates and visualization of the drone’s path.  

---

## **File Structure**
. Vecros_assignment/
├── notebooks/
│   └── important.txt
├── README.md  <-- This File
├── requirements.txt
└── src/
    ├── Drone_Simulation.py  <-- 2nd Script
    ├── path_Planning.py     <-- 1st Script
    



---
# 📌 README.md for 1st Problem Statement - Path Planning & Visualization

## 🛣️ 3D Path Planning & Visualization

This project implements a 3D grid path planning algorithm to find the shortest path between user-defined start and end points. The grid is created dynamically, and the paths are visualized in 3D to ensure no overlap between paths.

---

## 📌 Key Features:

- 🌐 **3D Grid Creation** (from (0,0,0) to (100,100,100))
- 🔍 **Shortest Path Calculation**
- 🚶‍♂️ **Path Non-Overlap**
- 📊 **3D Path Visualization**

---

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies

Make sure you have the required libraries installed. Use:

```bash
pip install matplotlib numpy


2️⃣ Run the Path Planning Script

Navigate to the src/ directory and run the script for path planning:

cd ~/vecros_assignment/src
python path_Planning.py

##**📌 Path Planning Workflow**

✔️ Creates a 3D grid with points (0,0,0) to (100,100,100)
✔️ Finds the shortest path between user-defined start and end points
✔️ Ensures paths do not overlap (Multiple paths allowed)
✔️ Visualizes the path in 3D using Matplotlib
✔️ Displays the computed path(s)
✔️ Saves 3D plot as path_visualization.png
📊 Path Visualization

The 3D flight path is saved in src/ as:

📍 path_visualization.png





# 📌 README.md for 2nd Problem Statement - Drone Mission Planning

## 🚁 Drone Mission Planning using DroneKit

This project involves planning a drone mission using a predefined set of waypoints and simulating the mission with DroneKit. The drone will land at the final waypoint, and the mission will be updated dynamically after 10 waypoints by adding a new waypoint 100 meters perpendicular to the current direction of travel.

---

## 📌 Key Features:

- 🛰️ **Waypoints Definition** (Dictionary with 'lat', 'lon', 'alt')
- 🚁 **Auto Mode Mission Planning** using DroneKit
- 🛣️ **Dynamic Waypoint Addition** after 10 waypoints
- 🕒 **Time and Distance Calculation** at each waypoint
- 📊 **2D Mission Path Visualization**

---

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies

Make sure you have the required libraries installed. Use:

```bash
pip install dronekit
pip install matplotlib
pip install dronekit matplotlib numpy

2️⃣ Start SITL Simulation

Before running the script, launch the ArduCopter SITL simulation:

sim_vehicle.py -v ArduCopter --console --map

    This will open MAVProxy console & live mission map.
    Wait for the message "Ready to fly" before proceeding.

3️⃣ Run the Drone Mission

Open a new terminal, navigate to the src/ directory, and execute:

cd ~/vecros_assignment/src
python Drone_Simulation.py

📌 Mission Workflow

✔️ Connects to Drone (SITL or real drone)
✔️ Arms the drone & takes off to 20m altitude
✔️ Follows 15 waypoints in AUTO mode
✔️ After 10th waypoint, dynamically adds a new waypoint 100m perpendicular to current direction
✔️ Prints real-time mission status (Estimated distance & time to completion)
✔️ Lands at the final waypoint
✔️ Plots & saves the flight path (path_visualization.png)
📊 Path Visualization

The 2D flight path is saved in src/ as:

📍 path_visualization.png

You can also check the live trajectory in MAVProxy or Mission Planner.
📁 Project Structure

vecros_assignment/
├── eeprom.bin
├── logs/
│   ├── 00000001.BIN
│   └── LASTLOG.TXT
├── mav.parm
├── mav.tlog
├── mav.tlog.raw
├── notebooks/
│   └── important.txt
├── README.md  <-- This File
├── requirements.txt
└── src/
    ├── Drone_Simulation.py  <-- 2nd Script
    ├── path_Planning.py     <-- 1st Script
    ├── path_visualization.png  <-- 2D Path Plot
    ├── terrain/
    │   └── S36E149.DAT

❗ Closing & Cleanup

After mission completion:

    Exit SITL properly by typing in MAVProxy:

    quit

    Ensure connection is closed in script (vehicle.close())

📢 Notes

    SITL must be running before executing Drone_Simulation.py.
    The drone will land automatically at the last waypoint.
    If using a real drone, replace "127.0.0.1:14550" with the actual telemetry port.







    ## 📢 Notes

### 1. **Drone Mission Planning (Path Planning Script)**
- **Mission Waypoints**: The script uses 15 predefined waypoints for the drone's mission.
  - After 10 waypoints, a new waypoint is added, which is 100 meters perpendicular to the current direction of travel.
  - The mission will then continue with the updated waypoints list.
- **Estimated Time and Distance**: The estimated time and distance to complete the mission are printed at every instance while traveling between waypoints.
- **Land at Final Waypoint**: The drone will land at the final waypoint after completing the mission path.

- **Input Cases**: For experimentation, you can modify and test different waypoint sequences using the `notebooks/important.tct` file.
  - Open the `.txt` file to explore multiple waypoint inputs with varying start and end points.
  - The file allows you to modify and test different paths or scenarios.
  - Once you select a new input case, rerun the mission planning script to observe the updated path and results.

### 2. **Drone Simulation Script**
- **Mission Simulation**: The `Drone_Simulation.py` script simulates a drone mission using different input cases and data to visualize the drone's movement and mission path.
- **Input Cases for Experimentation**: Similar to the path planning script, this script also has its own separate input cases.
  - Check the input data provided in the `notebooks/important.tct` file (or any other custom input files) to experiment with various scenarios and mission configurations.
  - You can modify the input cases in the provided `.txt` file and rerun the simulation script to test how the drone behaves with different configurations.

Both scripts have distinct input cases for experimenting with different waypoint paths, mission parameters, and scenarios. Make sure to modify the input cases in the respective files and rerun the scripts to test different configurations and obtain varied results.
