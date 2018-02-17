from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import threading
import cv2
import time
import frame


print("Threaded frames from pi camera module")
stream = frame.Frame(1 , "ProcessFrame")
stream.start()
time.sleep(2.0)

while 1:
    frame = stream.read()
    processed = stream.process(frame, (320,240))
    cv2.imshow("Frame", processed)
    key = cv2.waitKey(1) & 0xFF

cv2.destroyAllWindows()
stream.stop()
