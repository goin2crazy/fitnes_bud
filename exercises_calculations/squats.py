from .base import ExersicesBase
import random 
import cv2 
from time import sleep 

class SquatExsercise(ExersicesBase): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.name = 'Squat'

        self.down = False 
        self.up = False 

    def process_frame(self, pose_landmarks, frame):
        ps = pose_landmarks.landmark
        # Check for "down" position.  Using hips (23,24) and knees (25,26) is more robust.
        if all([True if landmark.y > 0.5 else False for landmark in ps[0:22]]):
            self.down = True

        # Check for "up" position, only if we were in the down position
        if self.down == True:
            if all([True if landmark.y < 0.5 else False for landmark in ps[0:22]]):
                self.up=True 

                # Draw the line
        if not self.down and not self.up:
            line_color = (0, 0, 255)  # Red
        elif self.down and not self.up:
            line_color = (0, 255, 255)  # Yellow
        elif self.down and self.up:
            line_color = (0, 255, 0)  # Green
            cv2.line(frame, (0, int(self.frame_height * 0.5)), (int(self.frame_width), int(self.frame_height * 0.5)), line_color, 5)
            sleep(0.5)

            # Done 
            self.down = False 
            self.up = False 
            return True 


        cv2.line(frame, (0, int(self.frame_height * 0.5)), (int(self.frame_width), int(self.frame_height * 0.5)), line_color, 5)
        return False 

if __name__ == "__main__":

    ex = SquatExsercise(random.randint(1,5)) # Run it once.  Removed the loop.
    ex.run()
