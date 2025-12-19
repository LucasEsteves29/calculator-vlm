# 🖐️ Finger Counter using MediaPipe + OpenCV

This project detects hands in real-time using OpenCV and MediaPipe, and counts how many fingers are raised on each hand. When both hands are detected, the application displays the total number of raised fingers.
---
## 📌 Features

Detects up to two hands

Counts raised fingers individually for left and right hands

Displays real-time finger count on screen

Computes finger posture based on MediaPipe landmark positions
---
## 🧠 How it works

The script:

Captures frames from the webcam

Uses MediaPipe Hands to detect hand landmarks

Computes relative landmark distances for each finger

Determines if fingers are up or down based on calibrated thresholds

Draws landmarks + text overlays on each frame
---
## 📷 Proper Hand Position

For optimal detection:

keep your hand around 30 cm (about 12 inches) away from the camera

fully extend fingers you want detected

keep the palm facing the camera

ensure good lighting

avoid blocking fingers with each other

This distance prevents distortion and improves landmark stability.
---
## ❌ Exit

Press the key: q
to close the application window safely.
---
## 📂 Project Structure Example
'
finger-counter/
│
├── finger_counter.py     # Main script
├── README.md
└── requirements.txt      # Optional
'
---
## ✨ Notes

Landmark thresholds used for classification may require adjustment depending on the user's hand size and camera quality.

Works best with webcams supporting 720p or higher.

Can be extended further for gesture recognition or sign language interpretation.