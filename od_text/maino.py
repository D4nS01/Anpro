import cv2
import numpy as np

# Load COCO class names
with open('coco.names.txt', 'r') as f:
    class_names = f.read().strip().split('\n')

# Load model and configuration
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Access webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Breite
cap.set(4, 720)  # Höhe

def non_max_suppression(boxes, confidences, threshold):
    # Convert to float
    boxes = boxes.astype(float)
    # Get indices of boxes sorted by confidence (high first)
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), confidences, 0.6, threshold)
    return indices

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare image for the model
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)

    # Get predictions
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    detections = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Collect all detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.65:  # Erhöhter Konfidenz-Schwellenwert
                center_x = int(obj[0] * frame.shape[1])
                center_y = int(obj[1] * frame.shape[0])
                width = int(obj[2] * frame.shape[1])
                height = int(obj[3] * frame.shape[0])
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                boxes.append([x, y, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    indices = non_max_suppression(np.array(boxes), confidences, 0.4)

    # Draw boxes for objects that survived NMS
    for i in indices:
        i = i[0] if isinstance(i, (list, np.ndarray)) else i
        box = boxes[i]
        x, y, w, h = box
        label = f"{class_names[class_ids[i]]}: {confidences[i]:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display image
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Erhöhter Wert für waitKey
        break

cap.release()
cv2.destroyAllWindows()
