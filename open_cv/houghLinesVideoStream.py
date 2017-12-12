import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


def process_frame(original_image):   # detect edges and draw hough lines
    # convert to greyscale
    greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # mask pixels that are not white
    masked_white_image = cv2.inRange(greyscale_image, 200, 255)
    # apply gaussian blur to image
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    # use canny edges
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)
    # region of interest points, (0,0 is top left)
    upper_top_left = [200, 220]
    upper_top_right = [440, 220]
    upper_lower_left = [0, 380]
    upper_lower_right = [640, 380]
    lower_top_left = [0, 380]
    lower_top_right = [640, 380]
    lower_bottom_left = [640, 480]
    lower_bottom_right = [0, 480]
    # mask image
    vertices = [np.array([upper_lower_left, upper_top_left, upper_top_right, upper_lower_right, lower_top_left, lower_top_right, lower_bottom_left, lower_bottom_right], dtype=np.int32)]
    mask = np.zeros_like(canny_edges_image)
    cv2.fillPoly(mask, vertices, 255)
    roi_image = cv2.bitwise_and(canny_edges_image, mask)
    # draw lines
    lines = cv2.HoughLinesP(roi_image, 2, np.pi/180, 20, np.array([]), minLineLength=50, maxLineGap=200)
    hough_lines_image = np.zeros((roi_image.shape[0], roi_image.shape[1], 3), dtype=np.uint8)
    center_line_image = cv2.line(hough_lines_image, (320, 0), (320, 480), (0, 255, 255), 5)  # (b,g,r)

    #for line in lines:
        #for x1, y1, x2, y2 in line:
            #cv2.line(hough_lines_image, (x1, y1), (x2, y2), [0, 0, 255], 5)

    result = cv2.addWeighted(center_line_image, 1, original_image, 1, 0.)
    return result


imageResolution = [640, 480]
camera = PiCamera()
camera.resolution = (imageResolution[0], imageResolution[1])    # set resolution of camera
camera.framerate = 30   # set framerate of camera
rawCapture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    final_image = process_frame(image)
    cv2.imshow("Processed Image", final_image)
    cv2.waitKey(0)

    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
