# Gesture Computer NUI Project

## Overview
The Gesture Computer NUI project aims to revolutionize how users interact with their computers by introducing an intuitive, gesture-based control system. This system allows users to perform common computing tasks through hand gestures, reducing dependency on traditional input devices like keyboards and mice.


## Developmental Stage - Controls to have
- Mouse movement
- Left click
- Right click
- Grab / hold left click
- Press enter
- Activate voice typing
- Create new desktop
- Delete desktop
- Shift to left desktop
- Shift to right desktop

## Developmental Stage - Feature details
- To activate the gesture control, face your palm towards the screen and open your hand.
- Move your hand to control the cursor. Press R0 to lock/unlock cursor control.
- For clicks and Enter key, use R1, R2, and R3 gestures respectively.
- To activate voice typing, press R4.
- Desktop management is controlled via tilting the activated hand.
  - **Create New Desktop**: Activate hand, R0 right, and right hand tilt right.
  - **Delete Desktop**: Activate hand, R0 right, and right hand tilt left.
  - **Shift Desktop**: Activate hand and tilt hand right/left without R0.
- Custom scripts and modes are controlled via the left hand (L0 to L4).

## Developmental Stage - Outline
All interface control is done with the right hand, while the left hand controls the mode of the right hand, including which package is activated.
Packages are created to import custom and case specific needs for the right hand, and up to 3 custom packages besides the main interface package can be installed at once, making them only a left hand gesture away from activation. You can only have one active package at a time.

## Clone Repo
- Use git command: `git clone https://github.com/TheCyberLocal/gesture-computer-nui`

## Contributing
Contributions to the Gesture Computer NUI project are welcome. Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

---

This README provides a comprehensive guide for users and contributors, outlining the project's purpose, setup, usage, customization options, and contributing guidelines.
