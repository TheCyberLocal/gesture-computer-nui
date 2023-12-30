# Gesture Computer NUI Project README

## Overview
Gesture Computer NUI is an innovative interface that allows users to control their computer using hand gestures. This project utilizes the `cv2` and `mediapipe` libraries to interpret hand gestures, with the left hand selecting operational modes and the right hand executing specific functions.

### R-Code and L-Code System
- Each finger corresponds to a specific code: 0 (thumb), 1 (index finger), 2 (middle finger), 3 (ring finger), 4 (pinky).
- The right hand (`R-Code`) is used for performing actions, while the left hand (`L-Code`) selects modes and controls program flow.

## Installation

### Prerequisites
- Python 3.x
- `cv2` and `mediapipe` libraries

### Clone the Repository
```bash
git clone https://github.com/yourusername/gesture-computer-nui.git
cd gesture-computer-nui
```

### Install Required Libraries
```bash
pip install opencv-python
pip install mediapipe
```

## Usage Instructions

### Activation
- To activate gesture recognition, face your open palm towards the screen.

### Exiting the Program
- Trigger both `l0` and `l3` (left thumb and ring finger) to exit the program.

### Selecting Modules
- Use the `l-codes` (left hand gestures) to switch between different modules for the right hand. For example, `l2` activates module 2.

### Right Hand Functions
- The right hand provides 5 primary finger functions (`r0` to `r4`), with additional sub-triggers for left and right tilt. 
- Each function has separate triggers for activation and deactivation, totalling at 15 activation and 15 deactivation functions for the right hand.

## Writing Custom Modules

### Creating a Module
1. Make a copy of customModTemplate.py with your desired name for your module (e.g., `myModule.py`).
2. Implement your desired functionality within the present functions. (The function names are self-explanatory)

### Connecting External Modules
1. Import your custom module to the main script as any module from 0 to 4.
   ```python
   import myModule as Module1
   ```

## Contributing
Contributions to enhance Gesture Computer NUI are welcome. Feel free to fork the repository, make changes, and submit pull requests.


---

This README provides a comprehensive guide for setting up, using, and extending the Gesture Computer NUI project. It outlines the system's fundamental concepts, installation instructions, usage guidelines, and steps for creating and integrating custom modules.