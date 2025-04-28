import math
import numpy as np
import airsim

class MotionController:
    def __init__(self, airsim_controller, movement_speed=2.0):
        self.airsim_controller = airsim_controller
        self.movement_speed = movement_speed
        self.min_distance = 3.0  # Minimum distance to maintain from target
        
    def move_towards_target(self, target_position):
        if target_position is None:
            self.airsim_controller.hover()
            return
            
        current_pose = self.airsim_controller.get_vehicle_pose()
        current_position = np.array([
            current_pose.position.x_val,
            current_pose.position.y_val,
            current_pose.position.z_val
        ])
        
        # If target_position is a numpy array
        if isinstance(target_position, np.ndarray):
            direction = target_position - current_position
        else:
            # If target_position is airsim.Vector3r
            direction = np.array([
                target_position.x_val - current_position[0],
                target_position.y_val - current_position[1],
                target_position.z_val - current_position[2]
            ])
        
        # Calculate distance to target
        distance = np.linalg.norm(direction)
        
        # Normalize direction
        if distance > 0:
            direction = direction / distance
            
        # Adjust velocity based on distance to target
        # Slow down as we get closer to the minimum distance
        if distance > self.min_distance:
            speed_factor = min(1.0, (distance - self.min_distance) / 5.0)
            velocity = direction * self.movement_speed * speed_factor
        else:
            # If too close, back up slightly
            velocity = -direction * self.movement_speed * 0.5
            
        # Move drone
        self.airsim_controller.move_by_velocity(
            velocity[0], velocity[1], velocity[2], 
            duration=0.5
        )
        
        return distance
    
    def orbit_target(self, target_position, orbit_radius=5.0, orbit_speed=0.5):
        """Orbit around a target point at a fixed radius"""
        if target_position is None:
            self.airsim_controller.hover()
            return
            
        current_pose = self.airsim_controller.get_vehicle_pose()
        current_position = np.array([
            current_pose.position.x_val,
            current_pose.position.y_val,
            current_pose.position.z_val
        ])
        
        # Convert target to numpy array if it's not already
        if not isinstance(target_position, np.ndarray):
            target_position = np.array([
                target_position.x_val,
                target_position.y_val,
                target_position.z_val
            ])
        
        # Vector from target to drone
        to_drone = current_position - target_position
        
        # Project onto XY plane for simpler orbiting
        to_drone_xy = np.array([to_drone[0], to_drone[1], 0])
        distance_xy = np.linalg.norm(to_drone_xy)
        
        if distance_xy > 0:
            # Normalize
            to_drone_xy = to_drone_xy / distance_xy
            
            # Calculate tangent vector (perpendicular to radial vector in XY plane)
            tangent = np.array([-to_drone_xy[1], to_drone_xy[0], 0])
            
            # Calculate radial adjustment to maintain orbit radius
            radial_error = distance_xy - orbit_radius
            radial_velocity = to_drone_xy * radial_error
            
            # Combine tangential and radial velocity
            velocity = tangent * orbit_speed + radial_velocity
            
            # Add Z component to maintain altitude
            velocity[2] = (target_position[2] - current_position[2]) * 0.5
            
            # Apply velocity
            self.airsim_controller.move_by_velocity(
                velocity[0], velocity[1], velocity[2], 
                duration=0.5
            )
        else:
            self.airsim_controller.hover()
