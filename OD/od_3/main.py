import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

# Initialize video capture from webcam
video = cv2.VideoCapture(0)

# Check if video capture is successful
if not video.isOpened():
    print("Error: Could not open video.")
    exit()

labels = []

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Perform object detection on the frame
    bbox, label, conf = cv.detect_common_objects(frame)

    # Draw bounding boxes around detected objects
    output_image = draw_bbox(frame, bbox, label, conf)

    # Display the output image
    cv2.imshow('Object Detection', output_image)

    # Collect unique labels detected in this frame
    for item in label:
        if item not in labels:
            labels.append(item)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resources
video.release()
cv2.destroyAllWindows()

# Print unique labels detected during the session
print("\nDetected objects:")
for label in labels:
    print(f"\t{label.title()}")

