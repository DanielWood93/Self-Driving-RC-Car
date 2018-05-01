"""frame.py

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
import cv2      # opencv
import time
import logging


class Frame(Thread):
    """Process camera images, convert to greyscale canny edge detection and center lines drawn"""

    def __init__(self, thread_id, thread_name, resolution=(320, 240), framerate=30):
        """Initialize pi camera settings and begin stream

        Args:
            thread_id (int): id of thread
            thread_name (str): name of thread
            resolution (int, int): (optional) resolution of camera image, (width, height) , defaults to (320, 240)
            framerate (int): (optional) framerate of stream, defaults to 30
        """
        logging.info('Frame: __init__')
        super(Frame, self).__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        """Start the thread's activity of update method"""
        logging.info('Frame: start')
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Update stream with next frame"""
        logging.info('Frame: update')
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
        return self.frame[120:240, 0:320]   # slice image and return lower half of frame

    def process(self, original):
        """Convert to greyscale, mask white pixels, gaussian blur, canny edge detection, draw horizontal center line

        Args:
            original (numpy.ndarray'): image to be processed
        Returns:
            canny_edges(numpy.ndarray'): processed image with edge detection
        """
        greyscale = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # convert to greyscale
        masked_white = cv2.inRange(greyscale, 200, 255)     # mask white pixels
        blurred = cv2.GaussianBlur(masked_white, (5, 5), 0)    # apply gaussian blur
        canny_edges = cv2.Canny(blurred, 50, 150)   # apply canny edge detection
        cv2.line(canny_edges, (160, 0), (160, 120), (255, 0, 255), 1)  # (b,g,r), add horizontal center line
        return canny_edges

    def save_image(self, filename, image):
        """Save image to file

        Args:
            filename (str): file name to save as (e.g. image.jpg)
            image (numpy.ndarray): image to save
        """
        logging.info('save_image')
        cv2.imwrite(filename, image)

    def stop_stream(self):
        """Stop stream"""
        logging.info('stop_stream')
        self.stopped = True


# for logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


def main():
    try:
        stream = Frame(1, "ProcessFrame")
        stream.start()
        time.sleep(1)
        while True:
            frame = stream.read()
            processed = stream.process(frame)

            cv2.imshow('Processed Frame', processed)
            cv2.waitKey(1) & 0xFF

    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')
        stream.stop_stream()
        cv2.destroyAllWindows()
        exit()


if __name__ == '__main__':
    main()
