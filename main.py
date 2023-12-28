"""
General framework has been implemented.
Last completed step was getting to logically call r0 and only when it was previously inactive.
"""

import mediapipe as mp
import cv2

class GestureControlInterface:
    def __init__(self):
        # Mapping gestures to their corresponding methods
        self.gesture_map = {
            'r0': self.r0,
            'r1': self.r1,
            'r2': self.r2,
            'r3': self.r3,
            'r4': self.r4,
        }
        # State variables to track changes in gestures
        self.previous_gestures = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False}
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic

    def detect_gesture(self, results):
        # Check if right hand landmarks are available
        if results.right_hand_landmarks:
            # Check the condition for the r0 gesture
            if results.right_hand_landmarks.landmark[8].x > results.right_hand_landmarks.landmark[4].x:
                if not self.previous_gestures['r0']:  # If r0 was not previously active
                    self.r0()  # Call r0 function
                    self.previous_gestures['r0'] = True  # Update the state
            else:
                self.previous_gestures['r0'] = False  # Reset the state when gesture is not active
        return None

    def run(self):
        cap = cv2.VideoCapture(0)  # Start capturing video
        with self.mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.6) as holistic:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(image)

                # Now pass the results to detect_gesture
                self.detect_gesture(results)  # Pass 'results' as an argument here


                # Draw the hand landmarks
                self.mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
                self.mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

                cv2.imshow('Gesture Control Interface', frame)
                if cv2.waitKey(1) == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def r0(self):
        # Implementation for the r0 gesture
        print('locked mouse position')

    def r1(self):
        # Implementation for the r1 gesture
        print('left clicked')

    def r2(self):
        # Implementation for the r2 gesture
        print('right clicked')

    def r3(self):
        # Implementation for the r3 gesture
        print('Pressed enter')

    def r4(self):
        # Implementation for the r4 gesture
        print('Voice typing activated')


# Set gesture interface class and run
gesture_interface = GestureControlInterface()
gesture_interface.run()
