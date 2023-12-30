"""
All custom modules are for the right hand since the left is meant to control which package the right uses.
Notice that each finger on your hand corresponds to an r-code or an l-code,
 r standing for right hand and l for left hand.
From thumb to pinky, the code is 0, 1, 2, 3, 4 respectively.

To provide a gesture, you must face your open palm towards the screen.
This will activate your hand, and the code will then search your hand for a gesture.
A gesture is recognized if a finger on your open palm bends between your palm and the monitor.

Notice the trigger activation and deactivation are not mutually exclusive to prevent activation flickering.
Left hand is not the interface, but chooses the right hand's modes and when to close the program.
Right hand is the interface, with 5 finger functions, one for each finger,
 and two additional sub-triggers, left and right tilt, totaling at 15 distinct functions for the right hand per mode.
Additionally, each function has two triggers, activation and deactivation, which both call their own functions,
allowing you to have different functionalities for activation and deactivation.

Basic Instructions:
Exit program by triggering both l0 and l3, (left thumb and ring finger).
Each l-code corresponds to a module number. For example, l2 sets right hand commands to use module 2.
As you can see below at import custom mods,
 you can change the names of the modules imported to your custom ones.
For example, "import myMod as Module1".

Once your modules are programed and imported to this main framework you are ready to have some fun!
"""

# import the necessary packages
import mediapipe as mp  # pip install mediapipe
import cv2  # pip install opencv-python

# import custom mods
import basicInterfaceV1_mod as Module0
import customMod1 as Module1
import customMod2 as Module2
import customMod3 as Module3
import customMod4 as Module4


class GestureControlInterface:
    def __init__(self):
        # State variables to track changes in gestures
        self.previous_gestures = {'l0': False, 'l1': False, 'l2': False, 'l3': False, 'l4': False,
                                  'r0_without_tilt': False, 'r1_without_tilt': False, 'r2_without_tilt': False,
                                  'r3_without_tilt': False, 'r4_without_tilt': False,
                                  'r0_tilted_right': False, 'r1_tilted_right': False, 'r2_tilted_right': False,
                                  'r3_tilted_right': False, 'r4_tilted_right': False,
                                  'r0_tilted_left': False, 'r1_tilted_left': False, 'r2_tilted_left': False,
                                  'r3_tilted_left': False, 'r4_tilted_left': False}
        self.mode = 0
        self.left_hand_active = False
        self.right_hand_active = False
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic

    # Check if left or right hand is active
    def check_if_active(self, results):

        # If there are left hand landmarks
        if results.left_hand_landmarks:

            # First check if left hand index finger either middle finger is up.
            if results.left_hand_landmarks.landmark[12].y < results.left_hand_landmarks.landmark[11].y or \
                    results.left_hand_landmarks.landmark[8].y < results.left_hand_landmarks.landmark[7].y:

                # Get the width and height of the left hand
                hand_width = abs(results.left_hand_landmarks.landmark[5].x - results.left_hand_landmarks.landmark[17].x)
                hand_height = results.left_hand_landmarks.landmark[0].y - results.left_hand_landmarks.landmark[5].y

                # If left hand height is greater than 1.5 times hand width and not active
                if hand_width * 1.5 < hand_height and not self.left_hand_active:
                    # Activate left hand
                    # Call function for activation
                    print('left hand activated')

                    # Update the state
                    self.left_hand_active = True

                # If left hand height is less than the hand width and is active
                elif hand_width >= hand_height and self.left_hand_active:
                    print('left hand deactivated')

                    # Update the previous state to deactivated
                    self.left_hand_active = False

                # If left hand is active then listen for gestures
                if self.left_hand_active:
                    # Call function for detecting gestures
                    self.detect_left_hand_gestures(results)

        # If no left hand landmarks and is active then make hand inactive
        elif not results.left_hand_landmarks and self.left_hand_active:
            print('left hand deactivated')

            # Update the previous state to deactivated
            self.left_hand_active = False

        # If there are right hand landmarks
        if results.right_hand_landmarks:

            # First check if right hand index finger either middle finger is up.
            if results.right_hand_landmarks.landmark[12].y < results.right_hand_landmarks.landmark[11].y or \
                    results.right_hand_landmarks.landmark[8].y < results.right_hand_landmarks.landmark[7].y:

                # Get the width and height of the right hand
                hand_width = abs(
                    results.right_hand_landmarks.landmark[5].x - results.right_hand_landmarks.landmark[17].x)
                hand_height = results.right_hand_landmarks.landmark[0].y - results.right_hand_landmarks.landmark[5].y

                # If right hand height is greater than 1.5 times hand width and previously was not active
                if hand_width * 1.5 < hand_height and not self.right_hand_active:
                    # Activate right hand
                    # Call function for activation
                    print('right hand activated')

                    # Update the state
                    self.right_hand_active = True

                elif hand_width >= hand_height and self.right_hand_active:
                    print('right hand deactivated')

                    # Update the previous state to deactivated
                    self.right_hand_active = False

                # If right hand is active then listen for gestures
                if self.right_hand_active:
                    # Call function for detecting gestures
                    self.detect_right_hand_gestures(results)

        # If no right hand landmarks and previously was active then make hand inactive
        elif not results.right_hand_landmarks and self.right_hand_active:
            print('right hand deactivated')

            # Update the previous state to deactivated
            self.right_hand_active = False

    def detect_left_hand_gestures(self, results):
        # If thumb's knuckle segment is over palm and previously was not activated
        if (results.left_hand_landmarks.landmark[3].x > results.left_hand_landmarks.landmark[5].x
                and not self.previous_gestures['l0']):

            print('l0 activated')

            # Update mode to 0
            self.mode = 0
            print('set mode to 0')

            # Update the previous state to activated
            self.previous_gestures['l0'] = True

        # If thumb's tip is not over palm and previously was activated
        elif (results.left_hand_landmarks.landmark[4].x < results.left_hand_landmarks.landmark[5].x
              and self.previous_gestures['l0']):

            print('l0 deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['l0'] = False

        # If index finger's tip is folded over palm and previously was not activated
        if (results.left_hand_landmarks.landmark[8].y > results.left_hand_landmarks.landmark[5].y
                and not self.previous_gestures['l1']):

            print('l1 activated')

            # Update mode to 1
            self.mode = 1
            print('set mode to 1')

            # Update the previous state to activated
            self.previous_gestures['l1'] = True

        # If index finger's middle segment is angled away from palm and previously was activated
        elif (results.left_hand_landmarks.landmark[7].y < results.left_hand_landmarks.landmark[6].y
              and self.previous_gestures['l1']):

            print('l1 deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['l1'] = False

        # If middle finger's tip is folded over palm and previously was not activated
        if (results.left_hand_landmarks.landmark[12].y > results.left_hand_landmarks.landmark[9].y
                and not self.previous_gestures['l2']):

            print('l2 activated')

            # Update mode to 2
            self.mode = 2
            print('set mode to 2')

            # Update the previous state to activated
            self.previous_gestures['l2'] = True

        # If middle finger's middle segment is angled away from palm and previously was activated
        elif (results.left_hand_landmarks.landmark[11].y < results.left_hand_landmarks.landmark[10].y
              and self.previous_gestures['l2']):

            print('l2 deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['l2'] = False

        # If ring finger's tip is folded over palm and previously was not activated
        if (results.left_hand_landmarks.landmark[16].y > results.left_hand_landmarks.landmark[13].y
                and not self.previous_gestures['l3']):

            print('l3 activated')

            # Update mode to 3
            self.mode = 3
            print('set mode to 3')

            # Update the previous state to activated
            self.previous_gestures['l3'] = True

        # If ring finger's middle segment is angled away from palm and previously was activated
        elif (results.left_hand_landmarks.landmark[15].y < results.left_hand_landmarks.landmark[14].y
              and self.previous_gestures['l3']):

            print('l3 deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['l3'] = False

        # If pinky's tip is folded over palm and previously was not activated
        if (results.left_hand_landmarks.landmark[20].y > results.left_hand_landmarks.landmark[17].y
                and not self.previous_gestures['l4']):

            print('l4 activated')

            # Update mode to 4
            self.mode = 4
            print('set mode to 4')

            # Update the previous state to activated
            self.previous_gestures['l4'] = True

        # If pinky's middle segment is angled away from palm and previously was activated
        elif (results.left_hand_landmarks.landmark[19].y < results.left_hand_landmarks.landmark[18].y
              and self.previous_gestures['l4']):

            print('l4 deactivated')

            # Update the previous state to deactivated
            self.previous_gestures['l4'] = False

        # If ring finger and thumb are folded over palm exit program
        # You are unlikely to accidentally exit using these two fingers
        if self.previous_gestures['l0'] and self.previous_gestures['l3']:
            # Destroy all the windows
            cv2.destroyAllWindows()
            exit(0)

    def detect_right_hand_gestures(self, results):

        # If right hand tilted right
        if results.right_hand_landmarks.landmark[5].x < results.right_hand_landmarks.landmark[0].x:
            # If thumb's tip crosses index finger's base knuckle horizontally and previously was not activated
            if (results.right_hand_landmarks.landmark[4].x < results.right_hand_landmarks.landmark[5].x
                    and not self.previous_gestures['r0_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_activated_tilted_right()
                if self.mode == 1:
                    Module1.r0_activated_tilted_right()
                if self.mode == 2:
                    Module2.r0_activated_tilted_right()
                if self.mode == 3:
                    Module3.r0_activated_tilted_right()
                if self.mode == 4:
                    Module4.r0_activated_tilted_right()

                # Update the previous state to activated
                self.previous_gestures['r0_tilted_right'] = True

            # If thumb's middle segment is angled away from palm and was previously activated
            elif (results.right_hand_landmarks.landmark[3].x > results.right_hand_landmarks.landmark[2].x
                  and self.previous_gestures['r0_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_deactivated_tilted_right()
                if self.mode == 1:
                    Module1.r0_deactivated_tilted_right()
                if self.mode == 2:
                    Module2.r0_deactivated_tilted_right()
                if self.mode == 3:
                    Module3.r0_deactivated_tilted_right()
                if self.mode == 4:
                    Module4.r0_deactivated_tilted_right()

                # Update the previous state to deactivated
                self.previous_gestures['r0_tilted_right'] = False

            # If index finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[8].y > results.right_hand_landmarks.landmark[5].y
                    and not self.previous_gestures['r1_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_activated_tilted_right()
                if self.mode == 1:
                    Module1.r1_activated_tilted_right()
                if self.mode == 2:
                    Module2.r1_activated_tilted_right()
                if self.mode == 3:
                    Module3.r1_activated_tilted_right()
                if self.mode == 4:
                    Module4.r1_activated_tilted_right()

                # Update the previous state to activated
                self.previous_gestures['r1_tilted_right'] = True

            # If index finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[7].y < results.right_hand_landmarks.landmark[6].y
                  and self.previous_gestures['r1_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_deactivated_tilted_right()
                if self.mode == 1:
                    Module1.r1_deactivated_tilted_right()
                if self.mode == 2:
                    Module2.r1_deactivated_tilted_right()
                if self.mode == 3:
                    Module3.r1_deactivated_tilted_right()
                if self.mode == 4:
                    Module4.r1_deactivated_tilted_right()

                # Update the previous state to deactivated
                self.previous_gestures['r1_tilted_right'] = False

            # If middle finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[12].y > results.right_hand_landmarks.landmark[9].y
                    and not self.previous_gestures['r2_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_activated_tilted_right()
                if self.mode == 1:
                    Module1.r2_activated_tilted_right()
                if self.mode == 2:
                    Module2.r2_activated_tilted_right()
                if self.mode == 3:
                    Module3.r2_activated_tilted_right()
                if self.mode == 4:
                    Module4.r2_activated_tilted_right()

                # Update the previous state to activated
                self.previous_gestures['r2_tilted_right'] = True

            # If middle finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[11].y < results.right_hand_landmarks.landmark[10].y
                  and self.previous_gestures['r2_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_deactivated_tilted_right()
                if self.mode == 1:
                    Module1.r2_deactivated_tilted_right()
                if self.mode == 2:
                    Module2.r2_deactivated_tilted_right()
                if self.mode == 3:
                    Module3.r2_deactivated_tilted_right()
                if self.mode == 4:
                    Module4.r2_deactivated_tilted_right()

                # Update the previous state to deactivated
                self.previous_gestures['r2_tilted_right'] = False

            # If ring finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[16].y > results.right_hand_landmarks.landmark[13].y
                    and not self.previous_gestures['r3_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_activated_tilted_right()
                if self.mode == 1:
                    Module1.r3_activated_tilted_right()
                if self.mode == 2:
                    Module2.r3_activated_tilted_right()
                if self.mode == 3:
                    Module3.r3_activated_tilted_right()
                if self.mode == 4:
                    Module4.r3_activated_tilted_right()

                # Update the previous state to activated
                self.previous_gestures['r3_tilted_right'] = True

            # If ring finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[15].y < results.right_hand_landmarks.landmark[14].y
                  and self.previous_gestures['r3_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_deactivated_tilted_right()
                if self.mode == 1:
                    Module1.r3_deactivated_tilted_right()
                if self.mode == 2:
                    Module2.r3_deactivated_tilted_right()
                if self.mode == 3:
                    Module3.r3_deactivated_tilted_right()
                if self.mode == 4:
                    Module4.r3_deactivated_tilted_right()

                # Update the previous state to deactivated
                self.previous_gestures['r3_tilted_right'] = False

            # If pinky's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[20].y > results.right_hand_landmarks.landmark[17].y
                    and not self.previous_gestures['r4_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_activated_tilted_right()
                if self.mode == 1:
                    Module1.r4_activated_tilted_right()
                if self.mode == 2:
                    Module2.r4_activated_tilted_right()
                if self.mode == 3:
                    Module3.r4_activated_tilted_right()
                if self.mode == 4:
                    Module4.r4_activated_tilted_right()

                # Update the previous state to activated
                self.previous_gestures['r4_tilted_right'] = True

            # If pinky's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[19].y < results.right_hand_landmarks.landmark[18].y
                  and self.previous_gestures['r4_tilted_right']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_deactivated_tilted_right()
                if self.mode == 1:
                    Module1.r4_deactivated_tilted_right()
                if self.mode == 2:
                    Module2.r4_deactivated_tilted_right()
                if self.mode == 3:
                    Module3.r4_deactivated_tilted_right()
                if self.mode == 4:
                    Module4.r4_deactivated_tilted_right()

                # Update the previous state to deactivated
                self.previous_gestures['r4_tilted_right'] = False

        # If right hand tilted left
        elif results.right_hand_landmarks.landmark[17].x > results.right_hand_landmarks.landmark[0].x:
            # If thumb's tip horizontally crosses the ring finger base knuckle and previously was not activated
            if (results.right_hand_landmarks.landmark[4].x < results.right_hand_landmarks.landmark[9].x
                    and not self.previous_gestures['r0_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_activated_tilted_left()
                if self.mode == 1:
                    Module1.r0_activated_tilted_left()
                if self.mode == 2:
                    Module2.r0_activated_tilted_left()
                if self.mode == 3:
                    Module3.r0_activated_tilted_left()
                if self.mode == 4:
                    Module4.r0_activated_tilted_left()

                # Update the previous state to activated
                self.previous_gestures['r0_tilted_left'] = True

            # If thumb's tip is not over palm and previously was activated
            elif (results.right_hand_landmarks.landmark[4].x > results.right_hand_landmarks.landmark[5].x
                  and self.previous_gestures['r0_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_deactivated_tilted_left()
                if self.mode == 1:
                    Module1.r0_deactivated_tilted_left()
                if self.mode == 2:
                    Module2.r0_deactivated_tilted_left()
                if self.mode == 3:
                    Module3.r0_deactivated_tilted_left()
                if self.mode == 4:
                    Module4.r0_deactivated_tilted_left()

                # Update the previous state to deactivated
                self.previous_gestures['r0_tilted_left'] = False

            # If index finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[8].y > results.right_hand_landmarks.landmark[5].y
                    and not self.previous_gestures['r1_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_activated_tilted_left()
                if self.mode == 1:
                    Module1.r1_activated_tilted_left()
                if self.mode == 2:
                    Module2.r1_activated_tilted_left()
                if self.mode == 3:
                    Module3.r1_activated_tilted_left()
                if self.mode == 4:
                    Module4.r1_activated_tilted_left()

                # Update the previous state to activated
                self.previous_gestures['r1_tilted_left'] = True

            # If index finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[7].y < results.right_hand_landmarks.landmark[5].y
                  and self.previous_gestures['r1_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_deactivated_tilted_left()
                if self.mode == 1:
                    Module1.r1_deactivated_tilted_left()
                if self.mode == 2:
                    Module2.r1_deactivated_tilted_left()
                if self.mode == 3:
                    Module3.r1_deactivated_tilted_left()
                if self.mode == 4:
                    Module4.r1_deactivated_tilted_left()

                # Update the previous state to deactivated
                self.previous_gestures['r1_tilted_left'] = False

            # If middle finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[12].y > results.right_hand_landmarks.landmark[9].y
                    and not self.previous_gestures['r2_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_activated_tilted_left()
                if self.mode == 1:
                    Module1.r2_activated_tilted_left()
                if self.mode == 2:
                    Module2.r2_activated_tilted_left()
                if self.mode == 3:
                    Module3.r2_activated_tilted_left()
                if self.mode == 4:
                    Module4.r2_activated_tilted_left()

                # Update the previous state to activated
                self.previous_gestures['r2_tilted_left'] = True

            # If middle finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[11].y < results.right_hand_landmarks.landmark[10].y
                  and self.previous_gestures['r2_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_deactivated_tilted_left()
                if self.mode == 1:
                    Module1.r2_deactivated_tilted_left()
                if self.mode == 2:
                    Module2.r2_deactivated_tilted_left()
                if self.mode == 3:
                    Module3.r2_deactivated_tilted_left()
                if self.mode == 4:
                    Module4.r2_deactivated_tilted_left()

                # Update the previous state to deactivated
                self.previous_gestures['r2_tilted_left'] = False

            # If ring finger's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[16].y > results.right_hand_landmarks.landmark[13].y
                    and not self.previous_gestures['r3_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_activated_tilted_left()
                if self.mode == 1:
                    Module1.r3_activated_tilted_left()
                if self.mode == 2:
                    Module2.r3_activated_tilted_left()
                if self.mode == 3:
                    Module3.r3_activated_tilted_left()
                if self.mode == 4:
                    Module4.r3_activated_tilted_left()

                # Update the previous state to activated
                self.previous_gestures['r3_tilted_left'] = True

            # If ring finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[15].y < results.right_hand_landmarks.landmark[14].y
                  and self.previous_gestures['r3_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_deactivated_tilted_left()
                if self.mode == 1:
                    Module1.r3_deactivated_tilted_left()
                if self.mode == 2:
                    Module2.r3_deactivated_tilted_left()
                if self.mode == 3:
                    Module3.r3_deactivated_tilted_left()
                if self.mode == 4:
                    Module4.r3_deactivated_tilted_left()

                # Update the previous state to deactivated
                self.previous_gestures['r3_tilted_left'] = False

            # If pinky's tip is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[20].y > results.right_hand_landmarks.landmark[17].y
                    and not self.previous_gestures['r4_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_activated_tilted_left()
                if self.mode == 1:
                    Module1.r4_activated_tilted_left()
                if self.mode == 2:
                    Module2.r4_activated_tilted_left()
                if self.mode == 3:
                    Module3.r4_activated_tilted_left()
                if self.mode == 4:
                    Module4.r4_activated_tilted_left()

                # Update the previous state to activated
                self.previous_gestures['r4_tilted_left'] = True

            # If pinky's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[19].y < results.right_hand_landmarks.landmark[18].y
                  and self.previous_gestures['r4_tilted_left']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_deactivated_tilted_left()
                if self.mode == 1:
                    Module1.r4_deactivated_tilted_left()
                if self.mode == 2:
                    Module2.r4_deactivated_tilted_left()
                if self.mode == 3:
                    Module3.r4_deactivated_tilted_left()
                if self.mode == 4:
                    Module4.r4_deactivated_tilted_left()

                # Update the previous state to deactivated
                self.previous_gestures['r4_tilted_left'] = False

        # If hand is not tilted
        else:
            # If thumb's knuckle is folded over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[3].x < results.right_hand_landmarks.landmark[5].x
                    and not self.previous_gestures['r0_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_activated_without_tilt()
                if self.mode == 1:
                    Module1.r0_activated_without_tilt()
                if self.mode == 2:
                    Module2.r0_activated_without_tilt()
                if self.mode == 3:
                    Module3.r0_activated_without_tilt()
                if self.mode == 4:
                    Module4.r0_activated_without_tilt()

                # Update the previous state to activated
                self.previous_gestures['r0_without_tilt'] = True

            # If thumb's tip is not over palm and previously was activated
            elif (results.right_hand_landmarks.landmark[4].x > results.right_hand_landmarks.landmark[5].x
                  and self.previous_gestures['r0_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r0_deactivated_without_tilt()
                if self.mode == 1:
                    Module1.r0_deactivated_without_tilt()
                if self.mode == 2:
                    Module2.r0_deactivated_without_tilt()
                if self.mode == 3:
                    Module3.r0_deactivated_without_tilt()
                if self.mode == 4:
                    Module4.r0_deactivated_without_tilt()

                # Update the previous state to deactivated
                self.previous_gestures['r0_without_tilt'] = False

            # If index finger's tip is over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[8].y > results.right_hand_landmarks.landmark[5].y
                    and not self.previous_gestures['r1_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_activated_without_tilt()
                if self.mode == 1:
                    Module1.r1_activated_without_tilt()
                if self.mode == 2:
                    Module2.r1_activated_without_tilt()
                if self.mode == 3:
                    Module3.r1_activated_without_tilt()
                if self.mode == 4:
                    Module4.r1_activated_without_tilt()

                # Update the previous state to activated
                self.previous_gestures['r1_without_tilt'] = True

            # If index finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[7].y < results.right_hand_landmarks.landmark[6].y
                  and self.previous_gestures['r1_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r1_deactivated_without_tilt()
                if self.mode == 1:
                    Module1.r1_deactivated_without_tilt()
                if self.mode == 2:
                    Module2.r1_deactivated_without_tilt()
                if self.mode == 3:
                    Module3.r1_deactivated_without_tilt()
                if self.mode == 4:
                    Module4.r1_deactivated_without_tilt()

                # Update the previous state to deactivated
                self.previous_gestures['r1_without_tilt'] = False

            # If middle finger's tip is over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[12].y > results.right_hand_landmarks.landmark[9].y
                    and not self.previous_gestures['r2_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_activated_without_tilt()
                if self.mode == 1:
                    Module1.r2_activated_without_tilt()
                if self.mode == 2:
                    Module2.r2_activated_without_tilt()
                if self.mode == 3:
                    Module3.r2_activated_without_tilt()
                if self.mode == 4:
                    Module4.r2_activated_without_tilt()

                # Update the previous state to activated
                self.previous_gestures['r2_without_tilt'] = True

            # If middle finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[11].y < results.right_hand_landmarks.landmark[10].y
                  and self.previous_gestures['r2_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r2_deactivated_without_tilt()
                if self.mode == 1:
                    Module1.r2_deactivated_without_tilt()
                if self.mode == 2:
                    Module2.r2_deactivated_without_tilt()
                if self.mode == 3:
                    Module3.r2_deactivated_without_tilt()
                if self.mode == 4:
                    Module4.r2_deactivated_without_tilt()

                # Update the previous state to deactivated
                self.previous_gestures['r2_without_tilt'] = False

            # If ring finger's tip is over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[16].y > results.right_hand_landmarks.landmark[13].y
                    and not self.previous_gestures['r3_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_activated_without_tilt()
                if self.mode == 1:
                    Module1.r3_activated_without_tilt()
                if self.mode == 2:
                    Module2.r3_activated_without_tilt()
                if self.mode == 3:
                    Module3.r3_activated_without_tilt()
                if self.mode == 4:
                    Module4.r3_activated_without_tilt()

                # Update the previous state to activated
                self.previous_gestures['r3_without_tilt'] = True

            # If ring finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[16].y < results.right_hand_landmarks.landmark[13].y
                  and self.previous_gestures['r3_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r3_deactivated_without_tilt()
                if self.mode == 1:
                    Module1.r3_deactivated_without_tilt()
                if self.mode == 2:
                    Module2.r3_deactivated_without_tilt()
                if self.mode == 3:
                    Module3.r3_deactivated_without_tilt()
                if self.mode == 4:
                    Module4.r3_deactivated_without_tilt()

                # Update the previous state to deactivated
                self.previous_gestures['r3_without_tilt'] = False

            # If pinky finger's tip is over palm and previously was not activated
            if (results.right_hand_landmarks.landmark[20].y > results.right_hand_landmarks.landmark[17].y
                    and not self.previous_gestures['r4_without_tilt']):

                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_activated_without_tilt()
                if self.mode == 1:
                    Module1.r4_activated_without_tilt()
                if self.mode == 2:
                    Module2.r4_activated_without_tilt()
                if self.mode == 3:
                    Module3.r4_activated_without_tilt()
                if self.mode == 4:
                    Module4.r4_activated_without_tilt()

                # Update the previous state to activated
                self.previous_gestures['r4_without_tilt'] = True

            # If pinky finger's middle segment is angled away from palm and previously was activated
            elif (results.right_hand_landmarks.landmark[20].y < results.right_hand_landmarks.landmark[17].y
                  and self.previous_gestures['r4_without_tilt']):
                
                # Chooses which module to run given the mode
                if self.mode == 0:
                    Module0.r4_deactivated_without_tilt()
                if self.mode == 1:
                    Module1.r4_deactivated_without_tilt()
                if self.mode == 2:
                    Module2.r4_deactivated_without_tilt()
                if self.mode == 3:
                    Module3.r4_deactivated_without_tilt()
                if self.mode == 4:
                    Module4.r4_deactivated_without_tilt()

                # Update the previous state to deactivated
                self.previous_gestures['r4_without_tilt'] = False

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


# Set gesture interface class and run
gesture_interface = GestureControlInterface()
gesture_interface.run()
