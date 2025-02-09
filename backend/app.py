import os
from flask import Flask, request, render_template, jsonify
import cv2
from ultralytics import YOLO

app = Flask(__name__)
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt") # LATAA MALLI

@app.route('/')
def home():
    return "Tervetuloa objektintunnistuspalveluun!"

if __name__ == '__main__':
    app.run(debug=True)
    