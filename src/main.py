import cv2

image_path = "data/testikuva.jpg"
image = cv2.imread(image_path)

if image is None:
    print(f"Virhe: Kuvaa ei löydy polusta {image_path}")
else:
    cv2.imwrite("testikuva_naytto.png", image)  # Tallennetaan kuva
    print("Kuva tallennettu nimellä testikuva_naytto.png, avaa se manuaalisesti.")