# Volume-Adjustment-Control
A vision-based real-time hand gesture system enables personalized, touchless volume control.

**OVERVIEW** : This project presents an intelligent vision-based real-time hand gesture recognition system that enables users to control volume levels using natural hand gestures eliminating the need for physical interaction. The system uses computer vision and deep learning techniques to recognize specific hand movements and adjusts volume dynamically in response. It is designed to be personalized, intuitive, and touchless, ensuring a hygienic and futuristic user experience.

<img width="497" height="211" alt="image" src="https://github.com/user-attachments/assets/326d4159-bdec-4dfa-8186-318b26a5c4fd" />


**OBJECIVE** : The aim of this project is to provide a touchless, intuitive, and interactive user interface that improves human-computer interaction by replacing traditional volume control mechanisms with hand gestures.

**HOW IT WORKS** : 
1. Capture Frame – The webcam continuously captures live frames.
2. Detect Hand – MediaPipe identifies the presence of hands and returns 21 landmarks.
3. Track Distance – The distance between the thumb tip and index finger tip is calculated.
4. Map to Volume – This distance is linearly mapped to the system’s volume range using PyCaw.
5. Visual Feedback – The system shows a volume bar and real-time percentage on the screen.
   
**FEATURES** :

1. Real-time hand detection and gesture tracking
2. Distance-based gesture mapping to control system volume
3. Touchless interaction enhances accessibility
4. Personalized tuning for different hand sizes and movement ranges
5. Smooth and responsive control via system API

**HOW TO RUN THE RPOJECT:**

**Install Dependencies:**
pip install opencv-python mediapipe pycaw numpy

**Run the Script**
```bash
python HandTrackingModule.py
