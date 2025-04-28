import cv2
import time
import numpy as np
import airsim

from airsim_controller import AirSimController
from object_detector import ObjectDetector
from motion_controller import MotionController
from input_handler import InputHandler

class TargetDetectionSystem:
    def __init__(self):
        self.airsim_controller = AirSimController()
        self.object_detector = ObjectDetector()
        self.motion_controller = MotionController(self.airsim_controller)
        self.input_handler = InputHandler()
        
        self.current_target = None
        self.target_world_position = None
        self.show_depth = True
        
    def initialize(self):
        print("Taking off...")
        self.airsim_controller.takeoff()
        print("Ready to detect targets!")
        
    def run(self):
        self.initialize()
        print("Starting 3D target detection system.")
        print("Controls:")
        print("  SPACE - Toggle tracking")
        print("  O - Toggle orbit mode")
        print("  ESC - Exit")
        
        try:
            while True:
                # Check user inputs
                inputs = self.input_handler.check_inputs()
                tracking_enabled = inputs['tracking_enabled']
                orbit_mode = inputs['orbit_mode']
                
                if self.input_handler.check_exit():
                    break
                
                # Get sensor data
                rgb_image = self.airsim_controller.get_rgb_image()
                depth_image = self.airsim_controller.get_depth_image()
                camera_info = self.airsim_controller.get_camera_info()
                
                # Detect objects
                detected_objects, annotated_image = self.object_detector.detect_objects(rgb_image, depth_image)
                
                # Display mode and status info on image
                status_text = f"Tracking: {'ON' if tracking_enabled else 'OFF'} | Mode: {'ORBIT' if orbit_mode else 'FOLLOW'}"
                cv2.putText(annotated_image, status_text, (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Show the annotated image
                cv2.imshow("AirSim 3D Target Detection", annotated_image)
                
                # Display depth visualization if available
                if self.show_depth and depth_image is not None:
                    # Normalize depth for visualization
                    depth_normalized = np.clip(depth_image, 0, 20) / 20.0  # Clip to 20m max
                    depth_visualized = (depth_normalized * 255).astype(np.uint8)
                    depth_colormap = cv2.applyColorMap(depth_visualized, cv2.COLORMAP_JET)
                    cv2.imshow("Depth Map", depth_colormap)
                
                # If tracking is enabled, find and follow nearest object
                if tracking_enabled and detected_objects:
                    nearest_object = self.object_detector.find_nearest_object(detected_objects)
                    if nearest_object:
                        self.current_target = nearest_object
                        
                        # Use depth for 3D position if available
                        if nearest_object["depth"] is not None:
                            # Convert pixel coordinates to world coordinates
                            drone_pose = self.airsim_controller.get_vehicle_pose()
                            world_pos = self.object_detector.pixel_to_world(
                                nearest_object["center"], 
                                nearest_object["depth"],
                                camera_info,
                                drone_pose
                            )
                            
                            # Store target position
                            self.target_world_position = world_pos
                            
                            # Move drone based on mode
                            if orbit_mode:
                                self.motion_controller.orbit_target(world_pos)
                                mode_str = "ORBIT"
                            else:
                                distance = self.motion_controller.move_towards_target(world_pos)
                                mode_str = "FOLLOW"
                                
                            # Print tracking info
                            print(f"[{mode_str}] Target at world position: ({world_pos[0]:.2f}, {world_pos[1]:.2f}, {world_pos[2]:.2f}) - Distance: {distance:.2f}m")
                        else:
                            print("Target detected but depth information unavailable")
                            self.airsim_controller.hover()
                else:
                    # Hover in place when not tracking
                    if not tracking_enabled:
                        self.airsim_controller.hover()
                
                time.sleep(0.05)  # Short delay to prevent CPU overuse
                
        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        cv2.destroyAllWindows()
        self.airsim_controller.shutdown()
        print("Target detection system terminated.")
