import cv2
import numpy as np
import math

class ObjectDetector:
    def __init__(self, min_contour_area=300):
        self.min_contour_area = min_contour_area
        self.target_position_3d = None
        
    def detect_objects(self, rgb_image, depth_image=None):
        # Process RGB image for initial detection
        gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_objects = []
        annotated_image = rgb_image.copy()
        
        for contour in contours:
            if cv2.contourArea(contour) > self.min_contour_area:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Calculate depth if available
                    depth = None
                    if depth_image is not None:
                        # Extract a small region around the center point to get better depth estimate
                        region_size = 5
                        x_start = max(0, cx - region_size)
                        x_end = min(depth_image.shape[1], cx + region_size)
                        y_start = max(0, cy - region_size)
                        y_end = min(depth_image.shape[0], cy + region_size)
                        
                        depth_region = depth_image[y_start:y_end, x_start:x_end]
                        # Filter out infinite values and get median
                        valid_depths = depth_region[~np.isinf(depth_region)]
                        if len(valid_depths) > 0:
                            depth = np.median(valid_depths)
                    
                    # Draw the contour and centroid
                    cv2.drawContours(annotated_image, [contour], -1, (0, 255, 0), 2)
                    cv2.circle(annotated_image, (cx, cy), 7, (0, 0, 255), -1)
                    
                    # Add depth text if available
                    if depth is not None:
                        depth_text = f"{depth:.2f}m"
                        cv2.putText(annotated_image, depth_text, (cx + 10, cy), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Store object data
                    object_data = {
                        "center": (cx, cy),
                        "area": cv2.contourArea(contour),
                        "contour": contour,
                        "depth": depth
                    }
                    detected_objects.append(object_data)
        
        return detected_objects, annotated_image
    
    def find_nearest_object(self, detected_objects):
        if not detected_objects:
            return None
        
        # If depth information is available, use it to find the nearest object
        has_depth = all(obj["depth"] is not None for obj in detected_objects)
        
        if has_depth:
            # Sort by depth (closest first)
            sorted_objects = sorted(detected_objects, key=lambda obj: obj["depth"])
        else:
            # Fall back to area-based sorting (larger area = closer)
            sorted_objects = sorted(detected_objects, key=lambda obj: obj["area"], reverse=True)
            
        return sorted_objects[0]
    
    def pixel_to_world(self, pixel_coords, depth, camera_info, drone_pose):
        """Convert pixel coordinates to 3D world coordinates using depth data"""
        # Extract camera parameters
        fx = fy = 320  # Default focal length (adjust based on actual AirSim camera settings)
        cx = 320  # Principal point x (default for 640x480 camera)
        cy = 240  # Principal point y (default for 640x480 camera)
        
        # If camera_info contains fov, recalculate fx, fy
        if hasattr(camera_info, 'fov'):
            fov_rad = math.radians(camera_info.fov)
            fx = fy = (cx * 2) / (2 * math.tan(fov_rad / 2))
        
        # Extract pixel coordinates
        px, py = pixel_coords
        
        # Convert from pixels to camera coordinates
        x = (px - cx) * depth / fx
        y = (py - cy) * depth / fy
        z = depth
        
        # Point in camera frame
        point_camera = np.array([x, y, z, 1.0])
        
        # Transform to drone body frame
        # For simplicity, assuming camera is aligned with drone body frame
        point_body = point_camera
        
        # Transform to world frame using drone pose
        drone_position = np.array([
            drone_pose.position.x_val, 
            drone_pose.position.y_val, 
            drone_pose.position.z_val
        ])
        
        # Convert quaternion to rotation matrix
        q = [
            drone_pose.orientation.w_val,
            drone_pose.orientation.x_val,
            drone_pose.orientation.y_val,
            drone_pose.orientation.z_val
        ]
        
        # Quaternion to rotation matrix
        # Formula from: https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        R = np.zeros((3, 3))
        R[0, 0] = 1 - 2 * (q[2]**2 + q[3]**2)
        R[0, 1] = 2 * (q[1]*q[2] - q[0]*q[3])
        R[0, 2] = 2 * (q[1]*q[3] + q[0]*q[2])
        R[1, 0] = 2 * (q[1]*q[2] + q[0]*q[3])
        R[1, 1] = 1 - 2 * (q[1]**2 + q[3]**2)
        R[1, 2] = 2 * (q[2]*q[3] - q[0]*q[1])
        R[2, 0] = 2 * (q[1]*q[3] - q[0]*q[2])
        R[2, 1] = 2 * (q[2]*q[3] + q[0]*q[1])
        R[2, 2] = 1 - 2 * (q[1]**2 + q[2]**2)
        
        # Apply rotation and translation
        point_world = np.dot(R, point_camera[:3]) + drone_position
        
        return point_world
