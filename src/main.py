import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

image_path = "data/testikuva.jpg"
image = cv2.imread(image_path)

if image is None:
    print(f"Virhe: Kuvaa ei löydy polusta {image_path}")
else:
    results = model(image_path)
    
    for result in results:
        result.show()
    print("Tunnistus valmis!")