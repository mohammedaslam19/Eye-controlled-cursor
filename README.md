# Eye-controlled-cursor

### Eye-Controlled Mouse and Navigation System

This project demonstrates a real-time eye-tracking system for hands-free cursor movement and navigation. Built using Python, OpenCV, Mediapipe, and PyAutoGUI, it utilizes facial landmarks to enable intuitive actions such as:

- **Cursor Movement**: Tracks gaze to control the on-screen cursor.
- **Scrolling**: Scroll up or down based on eye blink and gaze direction.
- **Navigation**: Execute browser navigation commands (`Go Back` and `Go Forward`) using mouth and eye gestures.
- **Blink Detection**: Recognizes eye blinks to trigger various actions.
- **Mouth Movement Detection**: Detects when the mouth is open to differentiate commands.

### Features
- Real-time facial landmark detection with Mediapipe.
- Gesture-based interactions for hands-free control.
- Customizable thresholds for blinking and scrolling sensitivity.
- Debugging output for easy calibration.

### Prerequisites
- Python 3.8 or later
- OpenCV, Mediapipe, PyAutoGUI

### Usage
1. Run the script and align your face with the webcam.
2. Use gaze and gestures to interact with the system.
3. Press `q` to exit the application.

This repository serves as an innovative approach to human-computer interaction, promoting accessibility and exploring the potential of computer vision for hands-free control.
