from picamera.array import PiRGBArray  # camera
from picamera import PiCamera  # camera
from threading import Thread
import cv2
import time
import datetime
from time import sleep
from approxeng.input.selectbinder import ControllerResource  # for controller
import os
import frame
import numpy as np
from pca9685_driver import Device  # for servo driver


def set_angle(pwm, channel, angle):
    """calculate servo angle"""
    pulse = (int(angle) * 2.5) + 150
    pwm.set_pwm(channel, int(pulse))

def capture_data(img):
    processed = stream.process(img, (320, 240))
    set_angle(pwm, 14, steering_angle)
    set_angle(pwm, 15, motor_angle)	
    output = [left_val, trigger_val, right_val]	#[left, forward, right]
    print(output)
    training_data.append([img, output])
    cv2.imshow("Frame", processed)
    cv2.waitKey(2)


pwm = Device(0x40)
pwm.set_pwm_frequency(60)
	
stream = frame.Frame(1, "SaveFrame")
stream.start()

steering_angle = 90
motor_angle = 133

left_val = 0
trigger_val = 0
right_val = 0

img_cap_location = "img_cap/"
npy_file = "dataset.npy"

time.sleep(1.0)

if os.path.isfile(npy_file):
    print("File exists, loading previous data")
    #training_data = list(np.load(npy_file))
    training_data = []
else:
    print("File does not exist!, starting new")
    training_data = []

print("--Ready--")
img = stream.read()
processed = stream.process(img, (320, 240))
while 1:
    try:
        with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1,dead_zone=0.1) as controller:
            print('Found a controller')
            while controller.connected:
				
                # left stick pressed (steering)
                if controller['lx'] != 0:
                    stick_val = int(controller['lx'])

                    if stick_val > 0:	# right
                        right_val = stick_val	#for array
                        steering_angle =  60
                        img = stream.read()
                        capture_data(img)

                    if stick_val < 0:	#left
                        left_val = stick_val*-1
                        steering_angle = 120
                        img = stream.read()
                        capture_data(img)

                # right trigger pressed (motor forward)
                if controller['rt'] != 0:
                    trigger_val = int(controller['rt'])
                    motor_angle = 0
                    img = stream.read()
                    capture_data(img)

                # left stick released (steering)
                if (controller['lx'] == 0) and (steering_angle != 90):
                    steering_angle = 90
                    left_val = 0
                    right_val = 0
                    img = stream.read()
                    capture_data(img)

                # right trigger released (motor)
                if (controller['rt'] == 0) and (motor_angle != 133):
                    motor_angle = 133
                    trigger_val = 0
                    img = stream.read()
                    capture_data(img)	

                if controller['square']:
                    print(training_data)
                    np.save(npy_file,training_data)
                    print("Saved training data: ", npy_file)


                if len(training_data) % 50 == 0:
                    print("---------------{}---------------".format(len(training_data)))
                    np.save(npy_file, training_data)
                    print("Saved training data: ", npy_file)

    except IOError:
        print('Waiting for controller...')
        sleep(1)

		