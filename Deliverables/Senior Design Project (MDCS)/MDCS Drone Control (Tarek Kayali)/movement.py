import airsim
import time

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

# Drone names (must match your settings.json config)
drones = ["Drone1", "Drone2", "Drone3", "Drone4"]

# Enable API control and arm
for drone in drones:
    client.enableApiControl(True, vehicle_name=drone)
    client.armDisarm(True, vehicle_name=drone)

# Take off
print("Taking off all drones...")
takeoffs = [client.takeoffAsync(vehicle_name=drone) for drone in drones]
for task in takeoffs:
    task.join()
time.sleep(2)

# Raise drones vertically to safe height (Z = -7)
print("Rising to cruising altitude...")
ascents = [client.moveToZAsync(-7, 2, vehicle_name=drone) for drone in drones]
for ascent in ascents:
    ascent.join()
time.sleep(1)

# Waypoints (x, y, z)
waypoints = [
    (10, 0, -7),
    (10, 10, -7),
    (0, 10, -7),
    (0, 0, -7)
]

# Fly through waypoints
for i, (x, y, z) in enumerate(waypoints):
    print(f"Moving to waypoint {i+1}: ({x}, {y}, {z})")
    moves = [client.moveToPositionAsync(x, y, z, 3, vehicle_name=drone) for drone in drones]
    for move in moves:
        move.join()
    time.sleep(2)

# Land
print("Landing all drones...")
lands = [client.landAsync(vehicle_name=drone) for drone in drones]
for land in lands:
    land.join()

# Disarm and release
for drone in drones:
    client.armDisarm(False, vehicle_name=drone)
    client.enableApiControl(False, vehicle_name=drone)

print("Mission complete for all drones!")
