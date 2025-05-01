import random
from time import sleep
import cv2
import mediapipe as mp
import numpy as np


def one_squat():
    """
    Visualizes pose landmarks from a camera feed and detects one squat.
    """
    # Initialize MediaPipe Pose solution
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False,  # Changed to False for video stream
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

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

    frame_height, frame_width = frame.shape[:2] # Get height and width

    down = False
    up = False
    squat_count = 0 # Initialize squat counter

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
        results = pose.process(rgb_frame)

        # Draw the pose landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            ps = results.pose_landmarks.landmark
            # Check for "down" position.  Using hips (23,24) and knees (25,26) is more robust.
            if all([True if landmark.y > 0.5 else False for landmark in ps[0:22]]):
                down = True

            # Check for "up" position, only if we were in the down position
            if down == True:
                if all([True if landmark.y < 0.5 else False for landmark in ps[0:22]]):
                    up=True 

        # Draw the line
        if not down and not up:
            line_color = (0, 0, 255)  # Red
        elif down and not up:
            line_color = (0, 255, 255)  # Yellow
        elif down and up:
            line_color = (0, 255, 0)  # Green
            cv2.line(frame, (0, int(frame_height * 0.5)), (int(frame_width), int(frame_height * 0.5)), line_color, 5)
            sleep(0.5)


        cv2.line(frame, (0, int(frame_height * 0.5)), (int(frame_width), int(frame_height * 0.5)), line_color, 5)

        # Display the squat count
        cv2.putText(frame, f"Squats: {squat_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        # Display the resulting frame
        cv2.imshow('Pose Comparison', frame)


        # Increment squat count
        if down and up:
            squat_count += 1
            down = False  # Reset for next squat
            up = False    # Reset up

        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows
    cap.release()
    pose.close() # Close the pose instance.
    cv2.destroyAllWindows()



if __name__ == "__main__":
    one_squat() # Run it once.  Removed the loop.
