Posture Detection App

A real-time posture detection tool that uses MediaPipe Pose Estimation, OpenCV, and Python to monitor your posture via webcam. If poor posture is detected (based on body angles), the system will play an audio warning to help you correct it instantly.

---

 Features

- Uses MediaPipe Pose to detect key body landmarks.
- Calculates the angle between shoulder, hip, and ankle to assess posture.
- Provides visual warnings on screen.
- Plays an audio alert if poor posture is detected.
- Runs in real-time with a webcam feed.

---

 How It Works

- Tracks key body joints: shoulders, hips, and ankles.
- Computes the angle at the hip joint:
  - If the angle < 90°, it’s assumed the person is slouching or leaning.
- If slouching is detected on either side:
  - A red warning message is shown.
  



 Requirements

- Python 3.7 – 3.11 (MediaPipe does not support Python 3.12+)
- Webcam
Install Dependencies

pip install opencv-python mediapipe playsound
