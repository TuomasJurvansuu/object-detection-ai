import cv2
import torch

print("OpenCV versio:", cv2.__version__)
print("PyTorch versio:", torch.__version__)
print("Onko CUDA käytössä:", torch.cuda.is_available())
