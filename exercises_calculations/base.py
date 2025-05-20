import random
from time import sleep, time
from datetime import datetime
import cv2
import mediapipe as mp
import numpy as np
import yaml
import json
import os


class ExersicesBase():
    def __init__(self,
                 required_count: int = None ,
                 callbacks = []):
        self.name = 'base'

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False,  # Changed to False for video stream
                                     min_detection_confidence=0.5,
                                     min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        self.callbacks = callbacks
        self.count = 0
        self.start_time = None
        self.end_time = None

        self.define_count(required_count)

    def define_count (self, required_count): 
        config = self._load_config()

        print(config)
        if required_count == None: 
            self.required_count = random.randint(config['normal_count']-3, config['normal_count']+2)
        elif type(required_count) == int: 
            self.required_count = required_count

    def visualize_pose(self, frame, results, *args, **kwargs):
        self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    def process_frame(self, pose_landmarks, frame,  *args, **kwargs):
        return False

    def process_done(self, pose_landmarks, frame,  *args, **kwargs):
        return

    def _load_config(self, config_path="config.yaml"):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file '{config_path}': {e}")
            return {}

    def save_in_history(self):
        config = self._load_config()
        dataset_path = config.get('dataset_path')

        if not dataset_path:
            print("Error: 'dataset_path' not defined in exercises_config.yaml.")
            return

        history_entry = {
            "type": self.name,
            "timestamp": datetime.now().isoformat(),
            "exercise": self.name,
            "count": self.count,
            "duration": round(self.end_time - self.start_time, 2) if self.start_time and self.end_time else None
        }

        if os.path.exists(dataset_path):
            try:
                with open(dataset_path, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(history_entry)

        try:
            with open(dataset_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Exercise data saved to: {dataset_path}")
        except IOError as e:
            print(f"Error writing to dataset file '{dataset_path}': {e}")

    def run(self):

        # Open the default camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        # Get the frame dimensions from the camera
        ret, frame = cap.read()  # Read a frame to get its dimensions
        if not ret:
            print("Error reading frame from camera")
            cap.release()
            return  # Exit the function if no frame is read

        self.frame_height, self.frame_width = frame.shape[:2] # Get height and width
        self.start_time = time()

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Flip the frame horizontally for a more natural selfie view
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with MediaPipe Pose
            results = self.pose.process(rgb_frame)

            if results.pose_landmarks:
                self.visualize_pose(frame, results)

                done = self.process_frame(results.pose_landmarks, frame)

                if done:
                    self.count += 1
                    for callback in self.callbacks:
                        callback(self.count, frame)

                    self.process_done(results.pose_landmarks, frame)

                    if self.count >= self.required_count:
                        self.end_time = time()
                        break

            # Display the squat count
            cv2.putText(frame, f"{self.name} count: {self.count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display the resulting frame
            cv2.imshow('Pose Comparison', frame)

                # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and destroy all windows
        cap.release()
        self.pose.close() # Close the pose instance.
        cv2.destroyAllWindows()

        self.save_in_history()