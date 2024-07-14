'''
Installation:
python3 -m venv --system-site-packages env
source env/bin/activate
pip3 install opencv-contrib-python
'''

import cv2
from picamera2 import Picamera2, Preview
import time
import numpy as np
from PIL import Image
from util import get_limits

# BGR values for lime green
lime = [15, 205, 100]

# Initialize camera
camera = Picamera2()
while True:
    camera.start()

    # Capture frame from camera and resize it
    frame = camera.capture_array()
    frame_small = cv2.resize(frame, (640, 480))
    rgb_img = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(frame_small, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=lime)
    mask = cv2.inRange(hsv_img, lowerLimit, upperLimit)

    # convert mask to image
    mask_img = Image.fromarray(mask)

    # Get bounding box of the object represented in the mask
    bbox = mask_img.getbbox()

    # If bounding box exists, get its coordinates and draw a rectangle over it
    if bbox:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imshow('frame', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

