"""frame.py
process image with masked region of interest image with canny edge detection and center lines drawn
Example:
    to use as a module
    'import frame'
    or
    to view processed stream
    '$ python3 frame.py'
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import numpy as np
import cv2
import time


class Frame:
    def __init__(self, thread_id, name, resolution=(320, 240), framerate=30):
        """Initialize pi camera settings and begin stream
        Args:
            thread_id: id of thread
            name: name of thread
            resolution: resolution of camera image, defaults to (320, 240)
            framerate: framerate of stream, defaults to 30
        """
        self.thread_id = thread_id
        self.name = name
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Update stream with next frame"""
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        """Read and return latest frame from stream"""
        return self.frame

    def process(self, original, res):
        """Define region of interest, convert to greyscale, mask image, canny edge detection, draw lines on image
        Args:
            original: image to be processed
            res: image resolution e.g. (320, 240)
        Returns:
            canny_edges: returns masked region of interest image with canny edge detection and center lines drawn
        """
        # define region of interest (bottom half of frame)
        top_left = [0, int(res[1] / 2)]
        top_right = [int(res[0]), int(res[1] / 2)]
        bottom_left = [res[0], res[1]]
        bottom_right = [0, res[1]]
        # convert original image to greyscale
        greyscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        # mask image
        vertices = [np.array([top_left, top_right, bottom_left, bottom_right], dtype=np.int32)]
        mask = np.zeros_like(greyscale)
        cv2.fillPoly(mask, vertices, 255)
        roi = cv2.bitwise_and(greyscale, mask)
        # edge detection
        masked_white = cv2.inRange(roi, 200, 255)
        gaussian_blurred = cv2.GaussianBlur(masked_white, (5, 5), 0)
        canny_edges = cv2.Canny(gaussian_blurred, 50, 150)
        # draw lines on top of image
        cv2.line(canny_edges, (160, 120), (160, 320), (255, 0, 255), 1)  # (b,g,r), horizontal center line
        cv2.line(canny_edges, (0, 120), (320, 120), (255, 0, 255), 1)  # (b,g,r), vertical center line
        return canny_edges

    def save_image(self, filename, image):
        """Save image to file
        Args:
            filename: file name to save as
            image: image to save
        """
        cv2.imwrite(filename, image)

    def stop_stream(self):
        """Stop stream"""
        self.stopped = True


def main():
    stream = Frame(1, "ProcessFrame")
    stream.start()
    time.sleep(2.0)
    while 1:
        frame = stream.read()
        processed = stream.process(frame, (320, 240))
        cv2.imshow("Processed Frame", processed)
        cv2.waitKey(1) & 0xFF
    cv2.destroyAllWindows()
    stream.stop_stream()
    print("-----END-----")
    exit()


if __name__ == '__main__':
    main()
