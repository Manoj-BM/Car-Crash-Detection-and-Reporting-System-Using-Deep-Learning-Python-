# Car-Crash-Detection-and-Reporting-System-Using-Deep-Learning-Python-
A Deep Learning–based Car Crash Detection and Reporting System using YOLOv8, OpenCV, and Flask.

Car Crash Detection and Reporting System Using Deep Learning

Project Overview
Th:is project presents a Deep Learning–based Car Crash Detection and Reporting System that automatically detects road accidents from video streams (CCTV, recorded video, or IP camera) using the YOLOv8 object detection model.
Once an accident is detected, the system highlights the crash with bounding boxes and sends an email notification to report the incident without human intervention.

Key Features:
Real-time car accident detection using YOLOv8
Works with uploaded videos and live IP camera streams
Draws bounding boxes with confidence scores
Automated accident email reporting
Web-based interface built using Flask

Technology Stack:
Programming Language: Python
Deep Learning Framework: PyTorch, Ultralytics YOLOv8
Computer Vision: OpenCV
Web Framework: Flask
Dataset & Annotation: Roboflow
Frontend: HTML, CSS, JavaScript


📂 Project Structure
├── app.py
├── models/
│   └── best.pt
├── templates/
│   ├── index.html
│   ├── login.html
│   └── yolo.html
├── static/
│   ├── uploads/
│   └── img/
├── requirements.txt
└── README.md

Dataset Description:
Dataset collected and annotated using Roboflow
Contains accident-related images and video frames
Images resized to 640×640
Dataset prepared in YOLOv8 format
Number of classes: 1 (Accident)

Working Methodology
Video input is provided (upload or live camera)
Video is converted into frames using OpenCV
Each frame is processed by YOLOv8
Accident regions are detected and highlighted
On detection, an email report is sent
Output video is displayed through the web interface

Results:
Accuracy: ~92%
Precision: ~91%
Recall: ~90%

Real-time detection with reliable performance

Limitations:
Performance depends on video quality
Requires good processing power for real-time inference
Limited dataset may affect rare accident scenarios

Future Enhancements:
GPS integration for exact accident location
Direct alerts to hospitals and traffic police
Multi-class accident severity detection
Integration with smart city surveillance systems

Author:
Manoj B M
MCA – Vidya Vikas Institute of Engineering & Technology
Project Guide: Prof. Sandeep N K

License

This project is for academic and learning purposes.
