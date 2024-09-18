import cv2
import numpy as np

def detect_traffic_light(image):
    """신호등 인식 로직"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 녹색 신호등 범위 설정
    green_lower = np.array([40, 40, 40])
    green_upper = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

  # 빨간색 신호등 범위
    red_lower = np.array([0, 50, 50])
    red_upper = np.array([10, 255, 255])
    mask_red = cv2.inRange(hsv, red_lower, red_upper)

    # 노란색 신호등 범위
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)


    if np.sum(mask_green) > 0:
        print("Green light detected!")
        return "green"
    elif np.sum(mask_red) > 0:
        print("Red light detected!")
        return "red"
    elif np.sum(mask_yellow) > 0:
        print("Yellow light detected!")
        return "yellow"
    else:
        print("No green light detected")
        return "none"

def detect_person(image):
    """사람 인식 로직 (YOLO 기반)"""
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Class 0: Person
                print("Person detected!")
                return True
    return False
