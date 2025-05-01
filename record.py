import cv2
import mediapipe as mp
import numpy as np
from time import sleep 

def save_landmarks_from_video(name, video_file_path):
    """
    Extracts pose landmarks from a video file and saves them to a numpy file.

    Args:
        name (str): The name of the person or activity in the video.  This will be used
            to create the name of the output file.
        video_file_path (str): The path to the video file.

    Returns:
        None: The function saves the landmarks to a .npy file.
    """
    # Initialize MediaPipe Pose solution
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Open the video file
    cap = cv2.VideoCapture(video_file_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {video_file_path}")
        return

    all_landmarks = []  # List to store landmarks from all frames

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)

        # Extract and store the pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            frame_landmarks = []
            for landmark in landmarks:
                frame_landmarks.append([landmark.x, landmark.y, landmark.z, landmark.visibility])
            all_landmarks.append(frame_landmarks)
            #  Optionally, you could draw the landmarks on the frame here, as in the original code
            #  mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Optionally, display the resulting frame (for debugging)
        # cv2.imshow('MediaPipe Pose', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release the video capture and destroy all windows
    cap.release()
    # cv2.destroyAllWindows() # Not needed if not displaying frames

    # Convert the list of landmarks to a numpy array
    all_landmarks_array = np.array(all_landmarks)

    # Save the landmarks to a numpy file
    output_file_name = f"{name}_landmarks.npy"
    np.save(output_file_name, all_landmarks_array)
    print(f"Landmarks saved to: {output_file_name}")



def visualize_pose_landmarks(landmarks_file_path):
    """
    Visualizes pose landmarks from a numpy file on a black background.

    Args:
        landmarks_file_path (str): The path to the .npy file containing the landmarks.
    """
    # Load the landmarks from the numpy file
    try:
        all_landmarks_array = np.load(landmarks_file_path)
    except FileNotFoundError:
        print(f"Error: Landmarks file not found at {landmarks_file_path}")
        return
    except Exception as e:
        print(f"Error loading landmarks: {e}")
        return

    # Initialize MediaPipe Pose drawing utility
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose # Needed for the connections

    # Determine the number of frames
    num_frames = all_landmarks_array.shape[0]

    # Create a black background image
    # Assuming the landmarks are normalized (0 to 1 range), we'll use a fixed size
    img_width = 640
    img_height = 480
    black_image = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    # Loop through each frame's landmarks
    for frame_idx in range(num_frames):
        frame_landmarks = all_landmarks_array[frame_idx]

        # Create a fresh black image for each frame.  This prevents drawing trails.
        black_image = np.zeros((img_height, img_width, 3), dtype=np.uint8)

        # Draw the landmarks on the black image
        if frame_landmarks is not None and len(frame_landmarks) > 0: # Check if landmarks were detected
            for i, landmark in enumerate(frame_landmarks):
                if i < len(mp_pose.PoseLandmark):
                  x, y = int(landmark[0] * img_width), int(landmark[1] * img_height)
                  cv2.circle(black_image, (x, y), 5, (255, 255, 255), -1) # Draw white circles

            connections = mp_pose.POSE_CONNECTIONS
            for connection in connections:
                start_point = frame_landmarks[connection[0]]
                end_point = frame_landmarks[connection[1]]
                if start_point is not None and end_point is not None:
                    start_x, start_y = int(start_point[0] * img_width), int(start_point[1] * img_height)
                    end_x, end_y = int(end_point[0] * img_width), int(end_point[1] * img_height)
                    cv2.line(black_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # Draw green lines

        # Display the image
        cv2.imshow('Pose Landmarks', black_image)
        sleep(0.06)

        # Wait for a short period or until a key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__": 
    data_name = str(input("Write down the name: "))

    if "landmarks" in data_name: 

        visualize_pose_landmarks(data_name)

    else: 

        video_path = str(input("Write there the video path pls: "))

        save_landmarks_from_video(data_name, video_path)