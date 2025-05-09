import math
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import matplotlib.pyplot as plt

class DroneMission:
    """
    Class to handle drone mission planning and execution using DroneKit API.
    
    Attributes:
        connection_string (str): The connection string to connect to the drone.
        vehicle (dronekit.Vehicle): The vehicle instance to interact with the drone.
        waypoints_dict (dict): A dictionary containing predefined waypoints with latitude, longitude, and altitude.
        waypoints (list): A list of LocationGlobalRelative objects representing the waypoints.
        size (int): Number of waypoints.
        latitudes (list): List of latitudes for plotting the path.
        longitudes (list): List of longitudes for plotting the path.
    """
    
    def __init__(self, connection_string="127.0.0.1:14550"):
        """
        Initializes the DroneMission class with the connection string and predefined waypoints.
        
        Args:
            connection_string (str): The connection string to connect to the drone (default is "127.0.0.1:14550").
        """
        self.connection_string = connection_string
        self.vehicle = None
        self.waypoints_dict = {
            # Outer Square
            1: {'lat': -35.363280, 'lon': 149.165220, 'alt': 20},
            2: {'lat': -35.363280, 'lon': 149.165250, 'alt': 20},
            3: {'lat': -35.363250, 'lon': 149.165250, 'alt': 20},
            4: {'lat': -35.363250, 'lon': 149.165220, 'alt': 20},
            5: {'lat': -35.363280, 'lon': 149.165220, 'alt': 20},  # Back to start

            # Middle Square
            6: {'lat': -35.363270, 'lon': 149.165225, 'alt': 20},
            7: {'lat': -35.363270, 'lon': 149.165245, 'alt': 20},
            8: {'lat': -35.363255, 'lon': 149.165245, 'alt': 20},
            9: {'lat': -35.363255, 'lon': 149.165225, 'alt': 20},
            10: {'lat': -35.363270, 'lon': 149.165225, 'alt': 20},  # Back to start

            # Inner Square
            11: {'lat': -35.363265, 'lon': 149.165230, 'alt': 20},
            12: {'lat': -35.363265, 'lon': 149.165240, 'alt': 20},
            13: {'lat': -35.363260, 'lon': 149.165240, 'alt': 20},
            14: {'lat': -35.363260, 'lon': 149.165230, 'alt': 20},
            15: {'lat': -35.363265, 'lon': 149.165230, 'alt': 20}  # Back to start
        }

        self.waypoints = [LocationGlobalRelative(wp['lat'], wp['lon'], wp['alt']) for wp in self.waypoints_dict.values()]
        self.size = len(self.waypoints)
        self.latitudes = []
        self.longitudes = []
        
    def connect_vehicle(self):
        """
        Connects to the vehicle using the specified connection string.
        
        Prints the connection status and vehicle mode.
        """
        print(f"Connecting to vehicle at {self.connection_string}")
        self.vehicle = connect(self.connection_string, wait_ready=True)
        print(f"Vehicle Mode: {self.vehicle.mode}")

    def arm_and_takeoff(self, altitude):
        """
        Arms the drone and takes off to the specified altitude.
        
        Args:
            altitude (float): The altitude in meters to which the drone will ascend.
        """
        print("Arming and taking off...")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        self.vehicle.simple_takeoff(altitude)

        while True:
            print(" Altitude:", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= altitude - 1:
                print("Reached target altitude")
                break
            time.sleep(1)

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculates the distance between two geographic coordinates using the Haversine formula.
        
        Args:
            lat1, lon1 (float): Latitude and longitude of the first point.
            lat2, lon2 (float): Latitude and longitude of the second point.
        
        Returns:
            float: The distance between the two points in meters.
        """
        R = 6371  # Radius of the Earth in kilometers
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c  # Distance in kilometers
        return distance * 1000  # Convert to meters

    def get_real_speed(self):
        """
        Retrieves the current speed of the vehicle.
        
        Returns:
            float: The current speed of the vehicle in meters per second.
        """
        return self.vehicle.groundspeed or 10  # Default to 10 m/s if no data

    def get_estimated_time(self, distance):
        """
        Estimates the time required to travel a given distance based on the current speed.
        
        Args:
            distance (float): The distance to travel in meters.
        
        Returns:
            float: The estimated time in seconds.
        """
        speed = self.get_real_speed()
        return distance / speed if speed > 0 else float('inf')

    def print_estimated_time_and_distance(self, current_location, next_wp):
        """
        Prints the estimated time and remaining distance to the next waypoint.
        
        Args:
            current_location (LocationGlobalRelative): The current location of the drone.
            next_wp (LocationGlobalRelative): The next waypoint to which the drone will travel.
        """
        distance = self.haversine(current_location.lat, current_location.lon, next_wp.lat, next_wp.lon)
        time_to_next_wp = self.get_estimated_time(distance)
        print(f"Remaining Distance: {distance:.2f} meters, Estimated Time: {time_to_next_wp:.2f} seconds")

    def plan_mission(self):
        """
        Plans and executes the drone mission, visiting each waypoint sequentially.
        """
        print("Starting mission...")
        self.vehicle.mode = VehicleMode("AUTO")
        temp = True

        for i in range(len(self.waypoints)+1):
            wp = self.waypoints[i]
            print(f"Going to waypoint {i + 1}: {wp}")

            self.latitudes.append(wp.lat)
            self.longitudes.append(wp.lon)

            if i < len(self.waypoints) - 1:
                self.print_estimated_time_and_distance(self.vehicle.location.global_relative_frame, self.waypoints[i + 1])

            self.vehicle.simple_goto(wp)
            start_time = time.time()

            while self.haversine(self.vehicle.location.global_relative_frame.lat,
                                 self.vehicle.location.global_relative_frame.lon,
                                 wp.lat, wp.lon) > 2:
                self.print_estimated_time_and_distance(self.vehicle.location.global_relative_frame, wp)
                time.sleep(1)
                if time.time() - start_time > 60:  # Timeout after 60 seconds
                    print("Timeout reached for waypoint, moving to next.")
                    break

            if i == 9 and temp:
                temp = False
                new_wp = self.get_perpendicular_waypoint(self.waypoints[self.size-2], self.waypoints[self.size-1])
                print(f"Adding final destination: {new_wp}")
                self.waypoints.append(new_wp)

        print("Landing at final destination...")
        self.vehicle.mode = VehicleMode("LAND")
        time.sleep(5)
        self.plot_path()

    def plot_path(self):
        """
        Plots the path taken by the drone using matplotlib.
        """
        plt.figure()
        plt.plot(self.longitudes, self.latitudes, marker='o')
        plt.title('Path of Travel')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.show()

    def get_perpendicular_waypoint(self, prev_wp, last_wp, distance=100):
        """
        Calculates a new waypoint that is perpendicular to the line formed by the previous and last waypoints.
        
        Args:
            prev_wp (LocationGlobalRelative): The previous waypoint.
            last_wp (LocationGlobalRelative): The last waypoint.
            distance (float): The distance to the new waypoint in meters (default is 100).
        
        Returns:
            LocationGlobalRelative: The calculated perpendicular waypoint.
        """
        d_lat = last_wp.lat - prev_wp.lat
        d_lon = last_wp.lon - prev_wp.lon
        norm = math.sqrt(d_lat**2 + d_lon**2)
        
        if norm == 0:
            return last_wp

        perp_lat = -d_lon / norm
        perp_lon = d_lat / norm

        new_lat = last_wp.lat + (perp_lat * distance / 1.113195e5)
        new_lon = last_wp.lon + (perp_lon * distance / 1.113195e5)
        
        return LocationGlobalRelative(new_lat, new_lon, last_wp.alt)

    def close_connection(self):
        """
        Closes the connection to the drone.
        """
        print("Closing vehicle connection...")
        self.vehicle.close()

if __name__ == "__main__":
    drone_mission = DroneMission()
    drone_mission.connect_vehicle()
    drone_mission.arm_and_takeoff(20)
    drone_mission.plan_mission()
    drone_mission.plot_path()
    drone_mission.close_connection()
