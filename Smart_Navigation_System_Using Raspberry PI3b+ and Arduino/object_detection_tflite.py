# import cv2
# import numpy as np
# import tflite_runtime.interpreter as tflite
# 
# class ObjectDetection:
#     def __init__(self, model_path, labels_path):
#         # Load the label map
#         with open(labels_path, 'r') as f:
#             self.labels = [line.strip() for line in f.readlines()]
# 
#         # Load the TFLite model and allocate tensors
#         self.interpreter = tflite.Interpreter(model_path=model_path)
#         self.interpreter.allocate_tensors()
# 
#         # Get input and output tensors
#         self.input_details = self.interpreter.get_input_details()
#         self.output_details = self.interpreter.get_output_details()
# 
#     def detect_objects(self, frame):
#         # Prepare the frame for prediction
#         input_shape = self.input_details[0]['shape']
#         frame_resized = cv2.resize(frame, (input_shape[1], input_shape[2]))
#         input_data = np.expand_dims(frame_resized, axis=0)
# 
#         # Perform the prediction
#         self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
#         self.interpreter.invoke()
# 
#         # Get the results
#         boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
#         classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # Class index of detected objects
#         scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # Confidence of detected objects
# 
#         detected_objects = []
# 
#         # Loop over the results and draw bounding boxes and labels
#         for i in range(len(scores)):
#             if scores[i] > 0.5:
#                 ymin, xmin, ymax, xmax = boxes[i]
#                 xmin = int(xmin * frame.shape[1])
#                 xmax = int(xmax * frame.shape[1])
#                 ymin = int(ymin * frame.shape[0])
#                 ymax = int(ymax * frame.shape[0])
#                 label = self.labels[int(classes[i])]
#                 detected_objects.append(label)
# 
#                 cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
# 
#         return frame, detected_objects


import os
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the label map
labels_path = '/home/sipho/Desktop/Final_Project/coco_labels.txt'
with open(labels_path, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Load the TFLite model and allocate tensors
model_path = '/home/sipho/Desktop/Final_Project/detect.tflite'
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details() 
output_details = interpreter.get_output_details()

# Initialize video stream
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Prepare the frame for prediction
    input_shape = input_details[0]['shape']
    frame_resized = cv2.resize(frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Perform the prediction
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get the results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

    # Loop over the results and draw bounding boxes and labels
    for i in range(len(scores)):
        if scores[i] > 0.5:
            ymin, xmin, ymax, xmax = boxes[i]
            xmin = int(xmin * frame.shape[1])
            xmax = int(xmax * frame.shape[1])
            ymin = int(ymin * frame.shape[0])
            ymax = int(ymax * frame.shape[0])
            label = labels[int(classes[i])]

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
#             cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
