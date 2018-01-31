import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np


def process_frame(original_image, res):
	##define region of interest (bottom half of frame)
    top_left = [0, int(res[1]/2)]
    top_right = [int(res[0]), int(res[1]/2)]
    bottom_left = [res[0], res[1]]
    bottom_right = [0, res[1]]
	
	##convert original image to greyscale
    greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	
	##mask image
    vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]
    mask = np.zeros_like(greyscale_image)
    cv2.fillPoly(mask, vertices, 255)
    roi_image = cv2.bitwise_and(greyscale_image, mask)
	
	##edge detection    
    masked_white_image = cv2.inRange(roi_image, 200, 255)
    gaussian_blurred_image = cv2.GaussianBlur(masked_white_image, (5, 5), 0)
    canny_edges_image = cv2.Canny(gaussian_blurred_image, 50, 150)

	##draw lines on top of image
    cv2.line(canny_edges_image, (160, 120), (160, 320), (255, 0, 255), 1)  # (b,g,r), horizontal center line
    cv2.line(canny_edges_image, (0, 120), (320, 120), (255, 0, 255), 1)  # (b,g,r), vertical center line
	
    return canny_edges_image


def main():
	##camera setup
    image_resolution = [320, 240]	
    camera = PiCamera()
    camera.resolution = (image_resolution[0], image_resolution[1])
    camera.framerate = 30  #30fps
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
