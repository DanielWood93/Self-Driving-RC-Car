import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


def process_frame(original_image):   ## detect edges and draw hough lines
    ## convert to greyscale
    greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    ## mask pixels that are not white
    masked_white_image = cv2.inRange(greyscale_image, 200, 255)
    ## apply gaussian blur to image
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    ## use canny edges
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)
	
    ## region of interest points, (0,0 is top left)
    ##320x240
	#top_left = [120, 120]
    #top_right = [200, 120]
    #bottom_left = [320, 240]
    #bottom_right = [0, 240]
	
	##640x480
    top_left = [240, 240]
    top_right = [400, 240]
    bottom_left = [640, 480]
    bottom_right = [0, 480]
	
    ## mask image
    vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]	
    mask = np.zeros_like(canny_edges_image)
    cv2.fillPoly(mask, vertices, 255)
    roi_image = cv2.bitwise_and(canny_edges_image, mask)
    #roi_image = cv2.bitwise_and(greyscale_image, mask)
	
    ## draw lines
    #lines = cv2.HoughLinesP(roi_image, 2, np.pi/180, 20, np.array([]), minLineLength=50, maxLineGap=200)
    #hough_lines_image = np.zeros((roi_image.shape[0], roi_image.shape[1], 3), dtype=np.uint8)
	
    #roi_line = cv2.line(hough_lines_image, (0, 220), (roi_image.shape[1], 220), (0, 255, 255), 1)  # (b,g,r)
    #car_center_line = cv2.line(roi_line, (roi_image.shape[1]/2, 360), (roi_image.shape[1]/2, roi_image.shape[1]), (0, 255, 255), 2)  # (b,g,r)
    #road_center_line = cv2.line(car_center_line, (150, 360), (490, 360), (255, 0, 255), 2)  # (b,g,r)
	
	## draw region of interest outline
    #pts = np.array([[120,120],[200,120],[320,240],[0,240]], np.int32)
    pts = np.array([[240,240],[400,240],[640,480],[0,480]], np.int32)
    pts = pts.reshape((-1,1,2))
    roi_outline = cv2.polylines(roi_image,[pts],True,(255,255,0))
	
    #center_line = cv2.line(hough_lines_image, (0, 220), (640, 220), (0, 255, 255), 1)  # (b,g,r)
    #center_line = cv2.line(roi_outline, (0, 220), (640, 220), (0, 255, 255), 1)  # (b,g,r)
    #car_center_line = cv2.line(center_line, (320, 360), (320, 640), (0, 255, 255), 2)  # (b,g,r)
    #road_center_line = cv2.line(car_center_line, (150, 360), (490, 360), (255, 0, 255), 2)  # (b,g,r)
	

    #for line in lines:
        #for x1, y1, x2, y2 in line:
            #cv2.line(hough_lines_image, (x1, y1), (x2, y2), [0, 0, 255], 5)
			
    #result = cv2.addWeighted(hough_lines_image, 1, original_image, 1, 0.)
    result = roi_outline
    return result


imageResolution = [640, 480]
#imageResolution = [320, 240]

camera = PiCamera()
camera.resolution = (imageResolution[0], imageResolution[1])    # set resolution of camera
camera.framerate = 30   # set framerate of camera
rawCapture = PiRGBArray(camera, size=(imageResolution[0], imageResolution[1]))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    final_image = process_frame(image)
    cv2.imshow("Processed Image", final_image)

    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
