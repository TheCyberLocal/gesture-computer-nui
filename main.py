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
        self.previous_gestures = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False,
                                  'l0': False, 'l1': False, 'l2': False, 'l3': False, 'l4': False,
                                  'mode': 0, 'left_hand_active': False, 'right_hand_active': False,
                                  'right_hand_tilted_right': False, 'right_hand_tilted_left': False}
        self.mode = 0
        self.left_hand_active = False
        self.right_hand_active = False
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic

    def check_if_active(self, results):

        # If there are left hand landmarks
        if results.left_hand_landmarks:

            # First check if left hand index finger either middle finger is up.
            if results.left_hand_landmarks.landmark[12].y < results.left_hand_landmarks.landmark[11].y or \
                    results.left_hand_landmarks.landmark[8].y < results.left_hand_landmarks.landmark[7].y:

                # Get the width and height of the left hand
                hand_width = abs(results.left_hand_landmarks.landmark[5].x - results.left_hand_landmarks.landmark[17].x)
                hand_height = results.left_hand_landmarks.landmark[0].y - results.left_hand_landmarks.landmark[5].y

                # If left hand height is greater than 1.5 times hand width and previously was not active
                if hand_width * 1.5 < hand_height and not self.previous_gestures['left_hand_active']:
                    # Activate left hand
                    # Call function for activation
                    print('left hand activated')

                    # Update the state
                    self.previous_gestures['left_hand_active'] = True

                elif hand_width >= hand_height and self.previous_gestures['left_hand_active']:
                    print('left hand deactivated')

                    # Update the previous state to deactivated
                    self.previous_gestures['left_hand_active'] = False

                # If left hand is active then listen for gestures
                if self.previous_gestures['left_hand_active']:
                    # Call function for detecting gestures
                    self.detect_left_hand_gestures(results)

        # If no left hand landmarks and previously was active then make hand inactive
        elif not results.left_hand_landmarks and self.previous_gestures['left_hand_active']:
            print('left hand deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['left_hand_active'] = False
            


        # If there are right hand landmarks
        if results.right_hand_landmarks:

            # First check if right hand index finger either middle finger is up.
            if results.right_hand_landmarks.landmark[12].y < results.right_hand_landmarks.landmark[11].y or \
                    results.right_hand_landmarks.landmark[8].y < results.right_hand_landmarks.landmark[7].y:

                # Get the width and height of the right hand
                hand_width = abs(results.right_hand_landmarks.landmark[5].x - results.right_hand_landmarks.landmark[17].x)
                hand_height = results.right_hand_landmarks.landmark[0].y - results.right_hand_landmarks.landmark[5].y

                # If right hand height is greater than 1.5 times hand width and previously was not active
                if hand_width * 1.5 < hand_height and not self.previous_gestures['right_hand_active']:
                    # Activate right hand
                    # Call function for activation
                    print('right hand activated')

                    # Update the state
                    self.previous_gestures['right_hand_active'] = True

                elif hand_width >= hand_height and self.previous_gestures['right_hand_active']:
                    print('right hand deactivated')

                    # Update the previous state to deactivated
                    self.previous_gestures['right_hand_active'] = False

                # If right hand is active then listen for gestures
                if self.previous_gestures['right_hand_active']:
                    # Call function for detecting gestures
                    self.detect_right_hand_gestures(results)

        # If no right hand landmarks and previously was active then make hand inactive
        elif not results.right_hand_landmarks and self.previous_gestures['right_hand_active']:
            print('right hand deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['right_hand_active'] = False

    def detect_left_hand_gestures(self, results):
        # Basic commands
        # If thumb is folded over palm and previously was not
        if (results.left_hand_landmarks.landmark[4].x > results.left_hand_landmarks.landmark[5].x
                and self.previous_gestures['l0'] is False):

            print('l0 activated')
            
            # Update mode to 0
            self.mode = 0
            
            # Update the previous state to activated
            self.previous_gestures['l0'] = True

        # If thumb is not folded over palm and previously was
        elif (results.left_hand_landmarks.landmark[4].x < results.left_hand_landmarks.landmark[5].x
                and self.previous_gestures['l0']):
            
            print('l0 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['l0'] = False

        # If index finger is folded over palm and previously was not
        if (results.left_hand_landmarks.landmark[8].y > results.left_hand_landmarks.landmark[5].y
                and self.previous_gestures['l1'] is False):
            
            print('l1 activated')
            
            # Update mode to 1
            self.mode = 1
            
            # Update the previous state to activated
            self.previous_gestures['l1'] = True

        # If index finger is not folded over palm and previously was
        elif (results.left_hand_landmarks.landmark[8].y < results.left_hand_landmarks.landmark[5].y
                and self.previous_gestures['l1']):
            
            print('l1 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['l1'] = False

        # If middle finger is folded over palm and previously was not
        if (results.left_hand_landmarks.landmark[12].y > results.left_hand_landmarks.landmark[9].y
                and self.previous_gestures['l2'] is False):
            
            print('l2 activated')
            
            # Update mode to 2
            self.mode = 2
            
            # Update the previous state to activated
            self.previous_gestures['l2'] = True

        # If middle finger is not folded over palm and previously was
        elif (results.left_hand_landmarks.landmark[12].y < results.left_hand_landmarks.landmark[9].y
                and self.previous_gestures['l2']):
            
            print('l2 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['l2'] = False

        # If ring finger is folded over palm and previously was not
        if (results.left_hand_landmarks.landmark[16].y > results.left_hand_landmarks.landmark[13].y
                and self.previous_gestures['l3'] is False):
            
            print('l3 activated')
            
            # Update mode to 3
            self.mode = 3
            
            # Update the previous state to activated
            self.previous_gestures['l3'] = True

        # If ring finger is not folded over palm and previously was
        elif (results.left_hand_landmarks.landmark[16].y < results.left_hand_landmarks.landmark[13].y
                and self.previous_gestures['l3']):
            
            print('l3 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['l3'] = False

        # If pinky finger is folded over palm and previously was not
        if (results.left_hand_landmarks.landmark[20].y > results.left_hand_landmarks.landmark[17].y
                and self.previous_gestures['l4'] is False):
            
            print('l4 activated')
            
            # Update mode to 4
            self.mode = 4
            
            # Update the previous state to activated
            self.previous_gestures['l4'] = True

        # If pinky finger is not folded over palm and previously was
        elif (results.left_hand_landmarks.landmark[20].y < results.left_hand_landmarks.landmark[17].y
                and self.previous_gestures['l4']):
            
            print('l4 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['l4'] = False

    def detect_right_hand_gestures(self, results):
        # If thumb is folded over palm and previously was not
        if (results.right_hand_landmarks.landmark[4].x < results.right_hand_landmarks.landmark[5].x
                and self.previous_gestures['r0'] is False):
            
            print('r0 activated')
            
            # Update the previous state to activated
            self.previous_gestures['r0'] = True

        # If thumb is not folded over palm and previously was
        elif (results.right_hand_landmarks.landmark[4].x > results.right_hand_landmarks.landmark[5].x
                and self.previous_gestures['r0']):
            
            print('r0 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['r0'] = False

        # If index finger is folded over palm and previously was not
        if (results.right_hand_landmarks.landmark[8].y > results.right_hand_landmarks.landmark[5].y
                and self.previous_gestures['r1'] is False):
            
            print('r1 activated')
            
            # Update the previous state to activated
            self.previous_gestures['r1'] = True

        # If index finger is not folded over palm and previously was
        elif (results.right_hand_landmarks.landmark[8].y < results.right_hand_landmarks.landmark[5].y
                and self.previous_gestures['r1']):
            
            print('r1 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['r1'] = False

        # If middle finger is folded over palm and previously was not
        if (results.right_hand_landmarks.landmark[12].y > results.right_hand_landmarks.landmark[9].y
                and self.previous_gestures['r2'] is False):
            
            print('r2 activated')
            
            # Update the previous state to activated
            self.previous_gestures['r2'] = True

        # If middle finger is not folded over palm and previously was
        elif (results.right_hand_landmarks.landmark[12].y < results.right_hand_landmarks.landmark[9].y
                and self.previous_gestures['r2']):
            
            print('r2 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['r2'] = False

        # If ring finger is folded over palm and previously was not
        if (results.right_hand_landmarks.landmark[16].y > results.right_hand_landmarks.landmark[13].y
                and self.previous_gestures['r3'] is False):
            
            print('r3 activated')
            
            # Update the previous state to activated
            self.previous_gestures['r3'] = True

        # If ring finger is not folded over palm and previously was
        elif (results.right_hand_landmarks.landmark[16].y < results.right_hand_landmarks.landmark[13].y
                and self.previous_gestures['r3']):
            
            print('r3 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['r3'] = False

        # If pinky finger is folded over palm and previously was not
        if (results.right_hand_landmarks.landmark[20].y > results.right_hand_landmarks.landmark[17].y
                and self.previous_gestures['r4'] is False):
            
            print('r4 activated')
            
            # Update the previous state to activated
            self.previous_gestures['r4'] = True

        # If pinky finger is not folded over palm and previously was
        elif (results.right_hand_landmarks.landmark[20].y < results.right_hand_landmarks.landmark[17].y
                and self.previous_gestures['r4']):
            
            print('r4 deactivated')
            
            # Update the previous state to deactivated
            self.previous_gestures['r4'] = False

        # Special commands
        # If hand tilted right and previously was not
        if (results.right_hand_landmarks.landmark[12].x < results.right_hand_landmarks.landmark[17].x
                and self.previous_gestures['right_hand_tilted_right'] is False):

            print('right hand tilted right activated')

            # Update the previous state to activated
            self.previous_gestures['right_hand_tilted_right'] = True

        # If hand is not tilted right and previously was
        elif (results.right_hand_landmarks.landmark[12].x > results.right_hand_landmarks.landmark[17].x
              and self.previous_gestures['right_hand_tilted_right']):

            print('right hand tilted right deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['right_hand_tilted_right'] = False

        # If hand tilted left and previously was not
        if (results.right_hand_landmarks.landmark[16].x > results.right_hand_landmarks.landmark[5].x
                and self.previous_gestures['right_hand_tilted_left'] is False):

            print('right hand tilted left activated')

            # Update the previous state to activated
            self.previous_gestures['right_hand_tilted_left'] = True

        # If hand is not tilted left and previously was
        elif (results.right_hand_landmarks.landmark[16].x < results.right_hand_landmarks.landmark[5].x
              and self.previous_gestures['right_hand_tilted_left']):

            print('right hand tilted left deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['right_hand_tilted_left'] = False

    def run(self):

        # Start capturing video from given source
        cap = cv2.VideoCapture(0)

        # Set mediapipe model with high confidence of 0.9 or greater
        with self.mp_holistic.Holistic(min_detection_confidence=0.9, min_tracking_confidence=0.9) as holistic:

            # Loop through every frame
            while cap.isOpened():

                # Read the frame
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert the frame to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Pass the image to mediapipe
                results = holistic.process(image)

                # Now pass the results to detect_gesture
                self.check_if_active(results)  # Pass 'results' as an argument here


                # Draw the hand landmarks
                self.mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
                self.mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

                # Show the frame
                cv2.imshow('Gesture Control Interface', frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) == ord('q'):
                    break

        # Release the video capture object
        cap.release()

        # Destroy all the windows
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
