"""
This script opens a webcam stream and applies the Holistic model on each frame
 to detect and visualize face and hand landmarks.
It displays the results in a window that updates in real-time.
The script stops when the 'q' key is pressed.
Ensure you have MediaPipe and OpenCV installed to run this script successfully.
"""

import cv2
import mediapipe as mp

# Initialize MediaPipe drawing and holistic modules
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Initialize Holistic model
with mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.6) as holistic:
    while cap.isOpened():
        ret, frame0 = cap.read()  # Read a frame from the webcam
        frame1 = frame0.copy()  # Copy the frame for drawing
        image = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB

        # Process the image and get the holistic results
        results = holistic.process(image)

        # Draw landmarks right hand, and left hand
        mp_drawing.draw_landmarks(frame1, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(frame1, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Print the coordinates of the right hand landmarks
        if results.right_hand_landmarks:
            for i, landmark in enumerate(results.right_hand_landmarks.landmark):
                print(f"Right hand landmark {i}: x={landmark.x}, y={landmark.y}, z={landmark.z}")

        # Display the processed image in a window
        cv2.imshow('frame1', frame1)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
