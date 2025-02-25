import os
from flask import Flask, request, render_template, send_file, jsonify, send_from_directory
import cv2
from ultralytics import YOLO

app = Flask(__name__, static_folder="../frontend", static_url_path="")
UPLOAD_FOLDER = "data/uploads"
PROCESSED_FOLDER = "data/processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")  # LATAA MALLI

@app.route("/", strict_slashes=False)
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/upload", methods=["POST"], strict_slashes=False)
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Ei tiedostoa ladattu"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Ei valittua tiedostoa"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    results = model(filepath)
    image = cv2.imread(filepath)
    detected_objects = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[int(box.cls[0])]
            confidence = round(box.conf[0].item() * 100, 1)
            detected_objects.append({"label": label, "confidence": f"{confidence}%"})

            # Piirrä laatikot kuvaan
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    processed_filepath = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}")
    cv2.imwrite(processed_filepath, image)

    return jsonify({
        "message": "Tunnistus valmis!",
        "objects": detected_objects,
        "image_url": f"/processed/{file.filename}"
    })

@app.route("/processed/<filename>")
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, f"processed_{filename}"), mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(debug=True)
