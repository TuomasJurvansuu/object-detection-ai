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
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Ei tiedostoa!", 400

    file = request.files["file"]
    if file.filename == "":
        return "Ei valittua tiedostoa!", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    results = model(filepath)
    detected_objects = []
    for result in results:
        for box in result.boxes:
            detected_objects.append(result.names[int(box.cls)])

    return jsonify({"message": "Tunnistus valmis!", "objects": detected_objects})

if __name__ == '__main__':
    app.run(debug=True)
    