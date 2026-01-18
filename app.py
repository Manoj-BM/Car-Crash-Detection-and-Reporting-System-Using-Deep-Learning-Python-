from flask import Flask, render_template, request, redirect, url_for, session

import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
import cv2

from csv import writer
from flask_material import Material
from flask import Flask, request, render_template, send_from_directory, Response, flash, redirect
from ultralytics import YOLO
import threading
import smtplib
import pygame
from flask import Flask, render_template, request, redirect, flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from ultralytics import YOLO

UPLOAD_FOLDER = 'static/uploads'
# Load the trained model

model = YOLO("best.pt")
classNames = ['Accident Detected']
yolo_model = YOLO("models/yolov8n.pt")

# EDA PKg
import pandas as pd 
import numpy as np 

# ML Pkg

app = Flask(__name__, static_url_path='/static')
Material(app)
app.secret_key = 'secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'mov', 'mkv'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Enter your database connection details below

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template('index.html')
    # User is not loggedin redirect to login page

@app.route('/about')
def about():
    return render_template('about.html')
    # User is not loggedin redirect to login page



@app.route('/yolo')
def yolo():
    return render_template('yolo.html')

@app.route('/',methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
                # If account exists in accounts table in out database
        if username=="admin" and password=="admin":
            # Create session data, we can access this data in other routes
            # Redirect to home page
            return render_template('index.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


# Email Configuration
SENDER_EMAIL = "user3737@.com"
RECEIVER_EMAIL = "user3737@.com"
PASSWORD = "ivtt ntwv ftuu dgzu"

# Email Sending Function
def send_alert_email(activity_type):
    try:
        subject = f"⚠ Alert: {activity_type} detected!"
        body = f"Urgent: The activity '{activity_type}' has been detected continuously for 20 frames."

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Alarm Sound Function
def play_alarm():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('alarm.wav')  # Make sure you have an alarm.mp3 file
        pygame.mixer.music.play()
        print("🚨 Alarm playing...")
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print(f"❌ Failed to play alarm: {e}")





@app.route('/yolo_video', methods=["POST"])
def yolo_video():
    if 'file' not in request.files:
        flash('⚠ No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('⚠ No video selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        video_path = save_path
        cap = cv2.VideoCapture(video_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Alert logic variables
        accident_counter = 0
        alert_sent = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # --- Accident Detection ---
            results = model(frame, stream=True)

            accident_detected_in_frame = False

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    class_name = classNames[cls]

                    if conf > 0.3:
                        accident_detected_in_frame = True

                        label = f"{class_name} {conf:.2f}"
                        color = (0, 0, 255)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                        cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # --- Counter Logic ---
            if accident_detected_in_frame:
                accident_counter += 1
            else:
                accident_counter = 0  # Reset counter if no accident detected in frame

            # --- Trigger Alert ---
            if accident_counter >= 5 and not alert_sent:
                print(f"🚨 Accident Detected for 20 continuous frames! Triggering Alarm and Email.")
                
                threading.Thread(target=send_alert_email, args=("Accident Detected",)).start()
                threading.Thread(target=play_alarm).start()

                alert_sent = True

            out.write(frame)
            cv2.imshow('Accident Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # Convert video to H.264
        converted_filename = "converted.mp4"
        converted_path = os.path.join(app.config['UPLOAD_FOLDER'], converted_filename).replace("\\", "/")
        os.system(f'ffmpeg -y -i "{output_path}" -vcodec libx264 -acodec aac "{converted_path}"')

        print(f"Prediction video saved at: {converted_path}")

        return render_template('yolo.html', aclass="Accident Detected", res=1, filename=converted_filename, video_url=f"/static/uploads/{converted_filename}")

    return "⚠ Invalid file type", 400


@app.route('/static/uploads/<filename>')
def serve_video(filename):
    """Serve video with correct MIME type."""
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(video_path):
        return "⚠ Video not found", 404  # Handle missing files gracefully

    return Response(open(video_path, "rb"), mimetype="video/mp4")



@app.route('/upload_video1', methods=["POST"])
def upload_video1():
    cv2.namedWindow('Accident Detection', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Accident Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cap = cv2.VideoCapture("http://000.00.00.000:0000/video")#0   http:here we want to add location /video

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Alert logic variables
    accident_counter = 0
    alert_sent = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # --- Accident Detection ---
        results = model(frame, stream=True)

        accident_detected_in_frame = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                class_name = classNames[cls]

                if conf > 0.3:
                    accident_detected_in_frame = True

                    label = f"{class_name} {conf:.2f}"
                    color = (0, 0, 255)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # --- Counter Logic ---
        if accident_detected_in_frame:
            accident_counter += 1
        else:
            accident_counter = 0  # Reset counter if no accident detected in frame

        # --- Trigger Alert ---
        if accident_counter >= 5 and not alert_sent:
            print(f"🚨 Accident Detected for 20 continuous frames! Triggering Alarm and Email.")
            
            threading.Thread(target=send_alert_email, args=("Accident Detected",)).start()
            threading.Thread(target=play_alarm).start()

            alert_sent = True

        out.write(frame)
        cv2.imshow('Accident Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return render_template('index.html')




if __name__ == '__main__':
	app.run(debug=True)
