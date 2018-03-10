"""data_collection.py
Collect training data for neural network.
Example:
    $ python3 data_collection.py
"""

from picamera.array import PiRGBArray  # for pi camera
from picamera import PiCamera  # for pi camera
from threading import Thread  # for threading
from approxeng.input.selectbinder import ControllerResource  # for xbox controller
from pca9685_driver import Device  # for PCA9685 servo driver
from time import sleep
import numpy as np
import cv2  # for opencv
import time
import datetime
import os
#import sys
import frame  # for image processing


class DataCapture(object):
    """Collect image and controller input data for neural network to .npy file
       collected data consists of:
       processed image with edge detection
       input data from controller, array of [left_val, motor_val, right_val] (0 or 1) e.g. [0,1,0] is forward
    """

    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name

        self.pwm = Device(0x40)  # setup PCA9685 servo driver
        self.pwm.set_pwm_frequency(60)  # setup PCA9685 servo driver

        self.steering_angle = 90  # initial angle of servo for steering
        self.motor_angle = 133  # initial angle of servo for motor

        self.npy_file = 'dataset.npy'  # numpy file for storing training data
        self.left_val = 0
        self.motor_val = 0
        self.right_val = 0
        self.training_data = []  # array for input data [left_val, motor_val, right_val]

        self.stream = frame.Frame(1, 'SaveFrame')
        self.stream.start()

        self.start()

    def start(self):
        Thread(target=self.gather_data(), args=()).start()
        return self

    def set_angle(self, channel, angle):
        """Calculate pulse width and set angle of servo motor
        Args:
            channel: channel of servo motor which is to be changed
            angle: angle to set servo motor to
        """
        pulse = (int(angle) * 2.5) + 150
        self.pwm.set_pwm(channel, int(pulse))

    def gather_data(self):
        """Loop to gather data using image data and controller input data"""
        if os.path.isfile(self.npy_file):
            print('DataSet file exists.. loading previous data')
            self.training_data = list(np.load(self.npy_file))
            # self.training_data = []
        else:
            print('DataSet file does not exist.. starting new file')
            self.training_data = []
        print('Training data samples: {}'.format(len(self.training_data)))

        print('Ready, connect controller and drive around to collect data ((X) controller button to stop collection)')
        while 1:
            try:
                with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1,
                                        dead_zone=0.1) as controller:
                    print('Found a controller')
                    while controller.connected:

                        # left stick moved (steering)
                        if controller['lx'] is not 0:
                            stick_val = int(controller['lx'])

                            if stick_val > 0:  # right
                                self.right_val = stick_val  # for array
                                self.steering_angle = 60
                                img = self.stream.read()
                                self.save_sample(img)

                            if stick_val < 0:  # left
                                self.left_val = stick_val * -1
                                self.steering_angle = 120
                                img = self.stream.read()
                                self.save_sample(img)

                        # right trigger moved (motor forward)
                        if controller['rt'] == 1:
                            self.motor_val = int(controller['rt'])
                            self.motor_angle = 125
                            img = self.stream.read()
                            self.save_sample(img)

                        # left stick released (steering centered)
                        if (controller['lx'] is 0) and (self.steering_angle is not 90):
                            self.steering_angle = 90
                            self.left_val = 0
                            self.right_val = 0
                            img = self.stream.read()
                            self.save_sample(img)

                        # right trigger released (motor stopped)
                        if (controller['rt'] is 0) and (self.motor_angle is not 133):
                            self.motor_angle = 133
                            self.motor_val = 0
                            img = self.stream.read()
                            self.save_sample(img)

                        # save dataset to npy file
                        if controller['square']:  # (X) button on Xbox One controller
                            self.stop_collection()

            except IOError:
                print('Waiting for controller...')
                sleep(1)

    def save_sample(self, img):
        """Save individual data sample
        sample consists of (processed image, input array)
        update angles of both motors (steering and motor)
        print input data array and show new processed image frame
        Args:
            img: image which is to be processed with edge detection
        """
        processed = self.stream.process(img, (320, 240))
        self.set_angle(14, self.steering_angle)
        self.set_angle(15, self.motor_angle)
        output = [self.left_val, self.motor_val, self.right_val]  # [left, forward, right]
        self.training_data.append([processed, output])
        print(output)
        cv2.imshow('Data Frame', processed)
        cv2.waitKey(1)

    def stop_collection(self):
        """Stop data capture"""
        print('-----Stopping Data Capture-----')
        self.save_dataset()
        cv2.destroyAllWindows()
        self.stream.stop()
        print("-----END-----")
        exit()

    def save_dataset(self):
        """Save complete dataset to npy file"""
        print("Saving training data to file: ", self.npy_file)
        np.save(self.npy_file, self.training_data)
        print('Training data samples: {}'.format(len(self.training_data)))


def main():
    dc = DataCapture(1, 'DataCapture')
    dc.start()


if __name__ == '__main__':
    main()
