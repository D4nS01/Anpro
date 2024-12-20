import cv2
import numpy as np

# Load COCO class names
with open('coco.names.txt', 'r') as f:
    class_names = f.read().strip().split('\n')

# Load model and configuration
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Access webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Width
cap.set(4, 720)  # Height

# Global variables
desired_object = None
detect_single_object = False
input_mode = False
input_text = ""


# Function to check if a point is inside a rectangle
def point_inside_rectangle(point, rect_top_left, rect_bottom_right):
    return rect_top_left[0] < point[0] < rect_bottom_right[0] and rect_top_left[1] < point[1] < rect_bottom_right[1]


# Function to calculate distance between two points
def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    center = (width // 2, height // 2)
    square_size = min(width, height) // 4
    square_top_left = (center[0] - square_size // 2, center[1] - square_size // 2)
    square_bottom_right = (center[0] + square_size // 2, center[1] + square_size // 2)

    # Draw the square only in specific mode
    if detect_single_object:
        cv2.rectangle(frame, square_top_left, square_bottom_right, (0, 255, 255), 2)

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
            if confidence > 0.55:  # Confidence threshold
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    score_threshold = 0.65
    nms_threshold = 0.4
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, nms_threshold)

    # List to store distances of desired objects
    desired_object_distances = []

    # Draw rectangles and guide camera
    for i in indices:
        i = i[0] if isinstance(i, (list, np.ndarray)) else i
        box = boxes[i]
        x, y, w, h = box
        label = class_names[class_ids[i]]

        # Calculate object center
        object_center = (x + w // 2, y + h // 2)

        if not detect_single_object or (detect_single_object and label == desired_object):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label}: {confidences[i]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

            if detect_single_object and label == desired_object:
                distance = calculate_distance(center, object_center)
                desired_object_distances.append((object_center, distance))

                # Guide camera
                dx = object_center[0] - center[0]
                dy = object_center[1] - center[1]

                if abs(dx) > 10:
                    direction_x = "Move camera right" if dx > 0 else "Move camera left"
                    cv2.putText(frame, direction_x, (10, height - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if abs(dy) > 10:
                    direction_y = "Move camera down" if dy > 0 else "Move camera up"
                    cv2.putText(frame, direction_y, (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display distance information for desired objects
    if detect_single_object and desired_object_distances:
        for idx, (obj_center, distance) in enumerate(desired_object_distances):
            cv2.putText(frame, f"Object {idx + 1}: {distance:.2f} pixels", (10, 120 + 30 * idx),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # Check if the object center is inside the square
            if point_inside_rectangle(obj_center, square_top_left, square_bottom_right):
                message = f"{desired_object} centered"
            else:
                message = f"{desired_object} is relatively behind the square"

            # Display the message
            cv2.putText(frame, message, (width // 2 - 100, height - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Mode display
    mode_text = f"Specific mode: {desired_object}" if detect_single_object else "all objects"
    cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if input_mode:
        cv2.putText(frame, "Specific object search is active: enter desired name", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Input: {input_text}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display image
    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Esc key
        if not input_mode:
            detect_single_object = not detect_single_object
            if detect_single_object:
                input_mode = True
                input_text = ""
            else:
                desired_object = None
        else:
            input_mode = False
            desired_object = input_text if input_text else None
    elif input_mode:
        if key == 13:  # Enter key
            input_mode = False
            desired_object = input_text if input_text else None
        elif key == 8:  # Backspace
            input_text = input_text[:-1]
        elif 32 <= key <= 126:  # Printable ASCII characters
            input_text += chr(key)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
