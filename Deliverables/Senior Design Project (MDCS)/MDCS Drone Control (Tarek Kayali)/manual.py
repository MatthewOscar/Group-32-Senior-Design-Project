import keyboard
import threading
import airsim
import time
import sys

# Global variable to track the currently selected drone
CURRENT_DRONE = "Drone1"
STOP_LISTENER = False  # Flag to stop the key listener thread

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

# Enable API control for all drones
for drone_name in ["Drone1", "Drone2", "Drone3", "Drone4"]:
    client.enableApiControl(True, vehicle_name=drone_name)
    print(f"API control enabled for {drone_name}")

def control_drone_with_keys():
    """Listen for key presses and control the drone accordingly."""
    global CURRENT_DRONE, STOP_LISTENER

    print("Key listener started. Use arrow keys to control the drone.")
    print("Press 1, 2, 3, or 4 to switch between drones.")

    while not STOP_LISTENER:
        try:
            if keyboard.is_pressed("up"):
                client.moveByVelocityAsync(2, 0, 0, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving forward")
            elif keyboard.is_pressed("down"):
                client.moveByVelocityAsync(-2, 0, 0, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving backward")
            elif keyboard.is_pressed("left"):
                client.moveByVelocityAsync(0, -2, 0, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving left")
            elif keyboard.is_pressed("right"):
                client.moveByVelocityAsync(0, 2, 0, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving right")
            elif keyboard.is_pressed("w"):
                client.moveByVelocityAsync(0, 0, -2, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving up")
            elif keyboard.is_pressed("s"):
                client.moveByVelocityAsync(0, 0, 2, 1, vehicle_name=CURRENT_DRONE)
                print(f"{CURRENT_DRONE} moving down")
            elif keyboard.is_pressed("1"):
                CURRENT_DRONE = "Drone1"
                print("Switched control to Drone1")
            elif keyboard.is_pressed("2"):
                CURRENT_DRONE = "Drone2"
                print("Switched control to Drone2")
            elif keyboard.is_pressed("3"):
                CURRENT_DRONE = "Drone3"
                print("Switched control to Drone3")
            elif keyboard.is_pressed("4"):
                CURRENT_DRONE = "Drone4"
                print("Switched control to Drone4")

            # Add a small delay to avoid excessive CPU usage
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in key listener: {e}")
            break

    print("Key listener stopped.")

def main():
    global STOP_LISTENER

    try:
        # Start the key listener in a separate thread
        key_listener_thread = threading.Thread(target=control_drone_with_keys, daemon=True)
        key_listener_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        STOP_LISTENER = True  # Set the flag to stop the key listener
        time.sleep(0.5)  # Give the thread some time to exit
        sys.exit(0)

if __name__ == "__main__":
    main()