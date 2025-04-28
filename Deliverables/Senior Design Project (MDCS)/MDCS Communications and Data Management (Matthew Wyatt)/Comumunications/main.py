import airsim
import cv2
import numpy as np
import time
import base64
import threading
from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to AirSim
client = airsim.MultirotorClient(timeout_value=60)
client.confirmConnection()
client.enableApiControl(True)  # synced line
client.armDisarm(True)  # synced line

# Camera name options: "0", "1", "2", "3", "4", "bottom_center", "front_center", "front_right", "front_left", "back_center"
global CAMERA_NAME
CAMERA_NAME = "1"

# Waypoints for navigation
waypoints = [  # Drone Control Sync
    (10, 0, -5),  # Drone Control Sync
    (10, 10, -5),  # Drone Control Sync
    (0, 10, -5),  # Drone Control Sync
    (0, 0, -5)  # Drone Control Sync
]

# Function to navigate through waypoints
def navigate_waypoints():  # Drone Control Sync
    print("Taking off...")  # Drone Control Sync
    client.takeoffAsync().join()  # Drone Control Sync
    time.sleep(2)  # Drone Control Sync

    for i, (x, y, z) in enumerate(waypoints):  # Drone Control Sync
        print(f"Moving to waypoint {i+1}: ({x}, {y}, {z})")  # Drone Control Sync
        client.moveToPositionAsync(x, y, z, 3).join()  # Drone Control Sync
        time.sleep(2)  # Drone Control Sync

    print("Landing...")  # Drone Control Sync
    client.landAsync().join()  # Drone Control Sync
    client.armDisarm(False)  # Drone Control Sync
    client.enableApiControl(False)  # Drone Control Sync
    print("Mission complete!")  # Drone Control Sync

# Function to get drone state
def get_drone_state(drone_name=""):
    try:
        state = client.getMultirotorState(vehicle_name=drone_name)
        position = state.kinematics_estimated.position
        linear_velocity = state.kinematics_estimated.linear_velocity

        if state.landed_state == airsim.LandedState.Landed:
            status = "Landed"
        elif state.landed_state == airsim.LandedState.Landing:
            status = "Landing"
        elif state.landed_state == airsim.LandedState.Flying:
            status = "Flying"
        elif state.landed_state == airsim.LandedState.Takeoff:
            status = "Taking Off"
        else:
            status = "Unknown"

        is_armed = state.rc_data.is_initialized and state.rc_data.is_valid
        collision_info = client.simGetCollisionInfo(vehicle_name=drone_name)
        has_collided = collision_info.has_collided

        elapsed_time = time.time() % 300
        battery = max(0, 100 - (elapsed_time / 300) * 30)

        return {
            "battery": battery,
            "position": [position.x_val, position.y_val, position.z_val],
            "velocity": [linear_velocity.x_val, linear_velocity.y_val, linear_velocity.z_val],
            "speed": np.sqrt(linear_velocity.x_val**2 + linear_velocity.y_val**2 + linear_velocity.z_val**2),
            "status": status,
            "is_armed": is_armed,
            "has_collided": has_collided,
            "altitude": -position.z_val
        }
    except Exception as e:
        print(f"Error getting drone state: {str(e)}")
        return {
            "battery": 0,
            "position": [0, 0, 0],
            "velocity": [0, 0, 0],
            "speed": 0,
            "status": "Disconnected",
            "is_armed": False,
            "has_collided": False,
            "altitude": 0
        }

# Function to generate camera frames
def generate_frames():
    lock = threading.Lock()  # Use a lock to ensure thread safety
    while True:
        try:
            with lock:
                # Request an image from the specified camera
                responses = client.simGetImages([airsim.ImageRequest(CAMERA_NAME, airsim.ImageType.Scene)])
                if responses and len(responses) > 0 and responses[0].width > 0 and responses[0].height > 0:
                    # Decode the image
                    img1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
                    img_rgb = cv2.imdecode(img1d, cv2.IMREAD_COLOR)  # Decode the image
                    img_rgb = cv2.resize(img_rgb, (640, 360))  # Resize to expected dimensions

                    # Encode the image as JPEG
                    _, jpeg = cv2.imencode('.jpg', img_rgb)
                    frame = jpeg.tobytes()

                    # Yield the frame for streaming
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    # Handle cases where no valid image is returned
                    error_img = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(error_img, "No camera feed available", (50, 240),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    _, jpeg = cv2.imencode('.jpg', error_img)
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            # Handle exceptions and generate an error frame
            error_img = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(error_img, f"Connection error: {str(e)}", (50, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            _, jpeg = cv2.imencode('.jpg', error_img)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drone_data')
def drone_data():
    return jsonify(get_drone_state())

@app.route('/drones')
def get_drones():
    """Fetch the state of all drones dynamically from AirSim."""
    drone_names = ["Drone1", "Drone2", "Drone3", "Drone4"]
    drones = []

    for i, drone_name in enumerate(drone_names, start=1):
        drone_state = get_drone_state(drone_name)
        drones.append({
            "id": i,
            "name": f"Drone {i}",
            **drone_state
        })

    return jsonify(drones)

@app.route('/navigate')
def navigate():
    navigate_waypoints()
    return jsonify({"message": "Navigation complete!"})

@app.route('/set_camera/<camera_name>', methods=['POST'])
def set_camera(camera_name):
    global CAMERA_NAME

    # Map drone IDs to AirSim camera names
    camera_mapping = {
        "1": "front_center",
        "2": "front_right",
        "3": "front_left"
    }

    if camera_name in camera_mapping:
        CAMERA_NAME = camera_mapping[camera_name]
        print(f"Camera changed to: {CAMERA_NAME}")
        return jsonify({"message": f"Camera set to {CAMERA_NAME}"})
    else:
        return jsonify({"error": "Invalid camera name"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)