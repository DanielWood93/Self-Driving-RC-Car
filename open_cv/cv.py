import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


def process_frame(original_image, res):
    pts = np.array([[(res[1]/2), (res[1]/2)], [400, (res[1]/2)], [res[0], res[1]], [1, res[1]]], np.int32)

    pts = pts.reshape((-1, 1, 2))
    roi_outline = cv2.polylines(original_image, [pts], True, (255, 255, 0))
	
    greyscale_image = cv2.cvtColor(roi_outline, cv2.COLOR_BGR2GRAY)
    masked_white_image = cv2.inRange(greyscale_image, 200, 255)
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)
	
	##region of interest outline
    top_left = [int(res[0]/2.666666666), int(res[0]/2.666666666)]
    top_right = [int(res[0]/1.6), int(res[0]/2.666666666)]
    bottom_left = [res[0], res[1]]
    bottom_right = [0, res[1]]

    ## mask image
    vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]
    mask = np.zeros_like(canny_edges_image)
    cv2.fillPoly(mask, vertices, 255)	#draw outline of roi

    #roi_image = cv2.bitwise_and(canny_edges_image, mask)	##roi edges
    roi_image = cv2.bitwise_and(greyscale_image, mask)  ##greyscale roi

    vertical_car_center_line = cv2.line(roi_image, (320, 360), (320, 640), (255, 0, 255), 1)  # (b,g,r)
    horizontal_road_line = cv2.line(vertical_car_center_line, (150, 360), (490, 360), (255, 0, 255), 1)  # (b,g,r)
	
    result = horizontal_road_line
    return result


def main():
    #image_resolution = [320, 240]
    image_resolution = [640, 480]
	
    camera = PiCamera()
    camera.resolution = (image_resolution[0], image_resolution[1])  # set resolution of camera
    camera.framerate = 30  # set framerate of camera
    rawCapture = PiRGBArray(camera, size=(image_resolution[0], image_resolution[1]))

    ##capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        final_image = process_frame(image, image_resolution)
        cv2.imshow("Processed Image", final_image)  # show processed image with edge detection

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break


if __name__ == '__main__':
    main()
