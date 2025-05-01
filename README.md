# Squat Detection with Python and MediaPipe

This code uses Python to watch you on your computer's camera and count how many squats you do! It's like having a virtual exercise buddy.

## What you need

* **A computer with a camera:** The code uses your computer's camera to see you.
* **Python:** This is the programming language the code is written in. You'll need to have it installed on your computer.
* **OpenCV:** This is a tool that helps Python work with your camera.
* **MediaPipe:** This is a clever tool that helps the code understand where your body is in the video.
* **Numpy:** This is a library for efficiently working with numerical data in Python.

## How it works

Here's how the code works, step-by-step:

1.  **Get ready:**
    * It opens your computer's camera.
    * It sets up MediaPipe to track your body movements.
2.  **Watch you:**
    * The code watches the video from your camera.
    * It uses MediaPipe to find your key body points (like your shoulders, hips, and knees).
3.  **Count your squats:**
    * The code looks at how your body moves to see if you're doing a squat.
    * It checks if you go "down" and then "up" again.
    * It counts each time you complete a squat.
4.  **Show you the results:**
    * The code displays the video from your camera on your screen.
    * It draws lines on the video to show your body pose.
    * It also shows a number on the screen, telling you how many squats it has counted.

## How to use it

1.  **Make sure you have everything installed:** You need Python, OpenCV, MediaPipe, and Numpy on your computer.
2.  **Run the code:** You'll need to run the Python code. This will open a window that shows the video from your camera.
3.  **Do your squats:** Stand in front of your camera and do your squats.
    4.  **See the count:** The code will show you how many squats it counts.

## What the code does

The code does the following:

* Opens your camera and gets video frames.
* Uses MediaPipe to find your body's pose in each frame.
* Draws lines and points on the video to show your pose.
* Checks if you are in the down position of a squat and then the up position.
* Counts the number of squats.
* Displays the video with the pose and squat count.

## In simple terms

This code is like a smart exercise tracker that uses your computer's camera to count your squats. It watches how your body moves and keeps track of how many times you go down and up. It then shows you the video and the squat count on your screen.

## Idea

Recently i came across to idea that it could be great to have something the can help me fixate my workout progress and motivate. 
Being a programmer despite very safe enviroment and comfort is very dangerous for health. 
So at the weekends i quickly remember that there was a lib tool for Google, called mediapipe, very fast, very efficient lib for pose estimation and etc. 

So now i have in plans to create something like cute fitness buddy that will block me from moveless hours of degrading with my laptop. 
✨I wanna make it prettty✨