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
import cv2
import time
import logging


class Frame(Thread):
    def __init__(self, thread_id, name, resolution=(320, 240), framerate=30):
        """Initialize pi camera settings and begin stream
        Args:
            thread_id: id of thread
            name: name of thread
            resolution: resolution of camera image, defaults to (320, 240)
            framerate: framerate of stream, defaults to 30
        """
        logging.info('__init__')
        super(Frame, self).__init__()
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
        logging.info('start')
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Update stream with next frame"""
        logging.info('starting self')
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

    def process(self, original):
        """Convert to greyscale, mask image, canny edge detection, draw horizontal center line
        Args:
            original: image to be processed
        Returns:
            canny_edges: returns masked region of interest image with canny edge detection and center lines drawn
        """
        greyscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # convert to greyscale
        masked_white = cv2.inRange(greyscale, 200, 255)     # mask white pixels of greyscale image
        blurred = cv2.GaussianBlur(masked_white, (5, 5), 0)    # apply gaussian blur
        canny_edges = cv2.Canny(blurred, 50, 150)   # apply canny edge detection
        cv2.line(canny_edges, (160, 0), (160, 120), (255, 0, 255), 1)  # (b,g,r), horizontal center line
        return canny_edges

    def save_image(self, filename, image):
        """Save image to file
        Args:
            filename: file name to save as
            image: image to save
        """
        logging.info('save_image')
        cv2.imwrite(filename, image)

    def stop_stream(self):
        """Stop stream"""
        logging.info('stop_stream')
        self.stopped = True


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


def main():
    try:
        stream = Frame(1, "ProcessFrame")
        stream.start()
        time.sleep(1)
        logging.info('start loop')
        while 1:
            frame = stream.read()
            halved = frame[120:240, 0:320]
            processed = stream.process(halved)

            cv2.imshow('Processed Frame', processed)
            cv2.waitKey(1) & 0xFF

    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')
        cv2.destroyAllWindows()
        stream.stop_stream()
        exit()


if __name__ == '__main__':
    main()