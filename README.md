# 🖱️ Virtual Mouse Control

A high-performance Virtual Mouse application built with Python, OpenCV, and MediaPipe. This project allows for touchless computer interaction by using hand gestures captured via a webcam to control the mouse cursor, click, scroll, and even take screenshots.

## ✨ Features
- **Precise Cursor Control:** Maps hand movements to screen coordinates with adjustable frame margins.
- **Smart Clicking:** Supports both single and double clicks based on the distance between the thumb and index finger.
- **Scroll Mode:** Activate scrolling by raising all four fingers.
- **Gesture Screenshots:** Take a screenshot instantly by making a fist (0 fingers raised).
- **Visual Feedback:** Real-time on-screen text overlays indicating the current action (Click, Scroll, etc.).

## 🛠️ Requirements

Before running the project, ensure you have Python installed and the following libraries:

```bash
pip install opencv-python mediapipe pyautogui numpy
