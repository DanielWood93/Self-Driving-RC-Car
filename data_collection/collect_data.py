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
import cv2
import os
import sys
sys.path.insert(0, '../')
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

        self.pwm = Device(0x40)  # setup PCA9685 servo driver device
        self.pwm.set_pwm_frequency(60)  # setup PCA9685 servo driver frequency

        self.steering_angle = 90  # set initial angle of servo for steering
        self.motor_angle = 133  # set initial angle of servo for motor

        # numpy data setup
        self.npy_file = 'datasets/dataset.npy'  # numpy file for storing training data
        self.left_val = 0       # [0,*,*]
        self.forward_val = 0    # [*,0,*]
        self.right_val = 0      # [*,*,0]
        self.training_data = []  # array for controller input data [left_val, motor_val, right_val]
        self.printed_length = False     # used to print length of training data

        self.stream = frame.Frame(1, 'SaveFrame')   # setup camera stream
        self.stream.start()     # start camera stream
        self.start()    # start data collection

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
                        self.set_angle(14, self.steering_angle)  # set angle for motors
                        self.set_angle(15, self.motor_angle)  # set angle for motors

                        # right trigger moved (motor forward)
                        if controller['rt'] == 1:
                            self.forward_val = int(controller['rt'])  # update forward val for input data array [*,0,*]
                            self.motor_angle = 125  # update servo angle for motor
                            self.printed_length = False
                            img = self.stream.read()    # read latest frame from camera stream
                            self.save_sample(img)       # save sample to dataset

                        # left stick moved (steering)
                        if controller['lx'] is not 0:
                            stick_val = int(controller['lx'])
                            if stick_val > 0:  # stick moved right
                                self.right_val = stick_val  # update value for input data array [*,*,1]
                                self.steering_angle = 60  # update servo angle for steering
                            if stick_val < 0:  # stick moved left
                                self.left_val = stick_val * -1    # update value for input data array [1,*,*]
                                self.steering_angle = 120  # update servo angle for steering

                        # left stick released (steering centered)
                        if (controller['lx'] is 0) and (self.steering_angle is not 90):
                            self.steering_angle = 90  # update servo angle for steering
                            self.left_val = 0     # update value for input data array [0,*,*]
                            self.right_val = 0    # update value for input data array [*,*,0]

                        # right trigger released (motor stopped)
                        if controller['rt'] is 0:
                            self.motor_angle = 133  # update servo angle for motor
                            self.forward_val = 0    # update value for input data array [*,0,*]

                        # save dataset to npy file
                        if controller['square']:  # (X) button on Xbox One controller
                            self.stop_collection()

                        if controller['triangle']:  # (Y) button on Xbox One controller
                            if not self.printed_length:     # to print length of data only once in loop
                                self.printed_length = True
                                print("Length of data: {}".format(len(self.training_data)))  # print current data length

                        if (len(self.training_data) % 100 == 0) and (len(self.training_data) is not 0):
                            print("100 more samples")

            except IOError:
                print('Waiting for controller...')
                sleep(1)

    def save_sample(self, img):
        """Save individual data sample
        sample consists of (processed image, input array)
        print input data array and show new processed image frame
        Args:
            img: image which is to be processed with edge detection
        """
        halved = img[120:240, 0:320]
        edges = self.stream.process(halved)  # edge detection
        output = [self.left_val, self.forward_val,
                  self.right_val]  # [left, forward, right] update array of controller input data
        self.training_data.append([edges, output])
        print(output)
        cv2.imshow('Data Collection Frame Preview', edges)
        cv2.waitKey(1)

    def stop_collection(self):
        """Stop data collection, save dataset, close camera preview, close stream"""
        print('-----Stopping Data Capture-----')
        self.save_dataset()
        cv2.destroyAllWindows()
        self.stream.stop_stream()
        print("-----END-----")
        exit()

    def save_dataset(self):
        """Save complete dataset to npy file"""
        print("Saving training data to file: ", self.npy_file)
        np.save(self.npy_file, self.training_data)
        print('Training data samples: {}'.format(len(self.training_data)))


def main():
    dc = DataCapture(1, 'DataCapture')


if __name__ == '__main__':
    main()
