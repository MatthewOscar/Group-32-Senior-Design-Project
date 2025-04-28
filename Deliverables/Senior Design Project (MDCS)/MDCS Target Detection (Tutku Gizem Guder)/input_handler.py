import keyboard
import time
import cv2

class InputHandler:
    def __init__(self):
        self.tracking_enabled = False
        self.orbit_mode = False
        self.last_key_time = time.time()
        self.key_cooldown = 0.3
        
    def check_inputs(self):
        current_time = time.time()
        
        # Toggle tracking
        if keyboard.is_pressed('space') and current_time - self.last_key_time > self.key_cooldown:
            self.tracking_enabled = not self.tracking_enabled
            status = "enabled" if self.tracking_enabled else "disabled"
            print(f"Tracking {status}")
            self.last_key_time = current_time
        
        # Toggle orbit mode
        if keyboard.is_pressed('o') and current_time - self.last_key_time > self.key_cooldown:
            self.orbit_mode = not self.orbit_mode
            status = "enabled" if self.orbit_mode else "disabled"
            print(f"Orbit mode {status}")
            self.last_key_time = current_time
            
        return {
            'tracking_enabled': self.tracking_enabled,
            'orbit_mode': self.orbit_mode
        }
    
    def check_exit(self):
        return cv2.waitKey(1) & 0xFF == 27  # ESC key
