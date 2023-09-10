#terminal command
#python yolo_video.py --video sample.mp4 --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt
from schema import SeatStatus, engine
import cv2
import argparse
import numpy as np
from datetime import datetime
from sqlalchemy.orm import sessionmaker


# Disable OpenCL to prevent possible compatibility issues
cv2.ocl.setUseOpenCL(False)

# Parse command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='path to input video')  # changed from '--image' to '--video'
ap.add_argument('-c', '--config', required=True, help='path to yolo config file')
ap.add_argument('-w', '--weights', required=True, help='path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True, help='path to text file containing class names')
args = ap.parse_args()

# Function to get output layers from YOLO neural network
def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

# Function to draw bounding boxes and labels on the image
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Load class names from the provided text file
with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

objects_to_find = ['person', 'bench', 'chair', 'couch', 'dining table']

# Initialize a list to store the indices
model_indices = []

# Find the indices of the objects in the class_names list
for obj in objects_to_find:
    if obj in classes:
        model_indices.append(classes.index(obj))

# Generate random colors for each class to be used for drawing bounding boxes
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Load the pre-trained YOLO model
net = cv2.dnn.readNet(args.weights, args.config)

# Open the video file
cap = cv2.VideoCapture(args.video)

frame_count = 0
# Set the desired frame interval (e.g., read one frame every 30 frames)
frame_interval = 30

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break  # if the video ended, break the loop
        # Increment the frame count
    frame_count += 1
    # Process the frame only if it's a multiple of the desired interval
    if frame_count % frame_interval == 0:

        Width = frame.shape[1]
        Height = frame.shape[0]
        scale = 0.00392

        # Preprocess the input image for YOLO model
        blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)

        # Set the preprocessed image as the input to the YOLO model
        net.setInput(blob)

        # Perform object detection using the YOLO model
        outs = net.forward(get_output_layers(net))

        # Initialize lists to store detected object information
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        # Process the output predictions and filter out low-confidence detections
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # Apply non-maximum suppression to eliminate overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        tables = []
        people = []
        vacant = True
        # Draw bounding boxes and labels on the image for detected objects
        for i in indices:
            try:
                box = boxes[i]
            except:
                i = i[0]
                box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            if class_ids[i] in model_indices:  # draws triangles ONLY around target objects
                if class_ids[i] == 60:  # 60 corresponds to 'dining table' class
                    tables.append([round(x), round(y), round(x + w), round(y + h)])
                if class_ids[i] == 0:
                    people.append([round(x), round(y), round(x + w), round(y + h)])

                draw_prediction(frame, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

        for t in range(len(tables)):
            for person in people:
                if (person[0] >= tables[t][0] and person[0] <= tables[t][2]) or (person[2] >= tables[t][0] and person[2] <= tables[t][2]) or (
                        person[1] >= tables[t][1] and person[1] >= tables[t][3]) or (person[3] >= tables[t][1] and person[3] <= tables[t][3]):
                    vacant = False
            new_entry = SeatStatus(table_id = t, number_of_people=len(people), vacancy_status=vacant, update_time=datetime.now())
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(new_entry)
            session.commit()
            session.close()

        # Display the resulting frame
        cv2.imshow('Video object detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit if 'q' is pressed
            break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
