"""import cv2
import numpy as np

yolo = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []

with open("coco.names", "r") as file:
    classes = [line.strip() for line in file.readlines()]
layer_names = yolo.getLayerNames()
output_layer = [layer_names[i[0]] - 1] for i in yolo.get

colorRed = (0,0,255)
colorGreen = (0, 255, 0)

#loading images
name = "test_faces.jpeg"
img = cv2.imread(name)"""