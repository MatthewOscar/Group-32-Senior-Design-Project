import airsim
import numpy as np
import math
import time

class AirSimController:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        
    def takeoff(self):
        self.client.takeoffAsync().join()
        
    def hover(self):
        self.client.hoverAsync()
        
    def move_by_velocity(self, vx, vy, vz, duration=1.0):
        self.client.moveByVelocityAsync(vx, vy, vz, duration)
        
    def get_vehicle_pose(self):
        return self.client.simGetVehiclePose()
        
    def get_rgb_image(self):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
        ])
        response = responses[0]
        
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)
        
        return img_rgb
    
    def get_depth_image(self):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True)
        ])
        response = responses[0]
        
        # Convert to depth map
        depth_img = airsim.list_to_2d_float_array(response.image_data_float, response.width, response.height)
        depth_img = depth_img.astype(np.float32)
        
        return depth_img
    
    def get_lidar_data(self):
        lidar_data = self.client.getLidarData()
        if (len(lidar_data.point_cloud) < 3):
            print("No lidar data received")
            return None
            
        points = np.array(lidar_data.point_cloud, dtype=np.float32).reshape(-1, 3)
        return points
    
    def get_camera_info(self):
        # Get camera parameters (field of view)
        camera_info = self.client.simGetCameraInfo("0")
        return camera_info
    
    def shutdown(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
        
    def get_objects(self):
        objects = self.client.simListSceneObjects()
        return objects
