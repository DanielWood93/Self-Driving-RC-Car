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


def map_value(val, low1, high1, low2, high2):
    """map values between controller and servo angle"""
    new_value = low2 + (high2 - low2) * (val - low1) / (high1 - low1)
    return new_value

	
def set_angle(pwm, channel, angle):
    """calculate servo angle"""
    pulse = (int(angle) * 2.5) + 150
    pwm.set_pwm(channel, int(pulse))


pwm = Device(0x40)
pwm.set_pwm_frequency(60)
	
stream = frame.Frame(1, "SaveFrame")
stream.start()

steering_angle = 90
motor_angle = 133
time.sleep(1.0)

img_cap_location = "img_cap/"
npy_file = "dataset.npy"

if os.path.isfile(npy_file):
    print("File exists, loading previous data")
    training_data = list(np.load(npy_file))
else:
    print("File does not exist!, starting fresh")
    training_data = []

print("--Ready--")
while 1:
    #img = stream.read()
    #processed = stream.process(img, (320, 240))		##frame is black, need to fix it
    #cv2.imshow("Frame", processed)
    #key = cv2.waitKey(1) & 0xFF
	
    try:
        with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1,dead_zone=0.1) as controller:
            print('Found a controller')
            while controller.connected:
                img = stream.read()
                processed = stream.process(img, (320, 240))
                #cv2.imshow("Frame", processed)
                #key = cv2.waitKey(1) & 0xFF
			
                set_angle(pwm, 14, steering_angle)
                set_angle(pwm, 15, motor_angle)
				
                # left stick pressed (steering)
                if controller['lx'] != 0:
                    stick_val = round(controller['lx'], 1)
                    if stick_val > 0:	# right
                        output = [0, 0, stick_val]	#[left, forward, right]
                        training_data.append([img, output])
                        #print(output)
                        mapped_steering_value = int(map_value(stick_val, 0, 1, 90, 60))	#(120, 60) then (120,0)
                        if mapped_steering_value != steering_angle:
                            steering_angle = mapped_steering_value
                            print("R({}%) - S: {}, M: {}".format(stick_val*100, steering_angle, motor_angle))
								
							
                    if stick_val < 0:	#left

                        stick_val = stick_val*-1
                        mapped_steering_value = int(map_value(stick_val, 0, 1, 90, 120))
                        if mapped_steering_value != steering_angle:
                            steering_angle = mapped_steering_value
                            print("L({}%) - S: {}, M: {}".format(stick_val*100, steering_angle, motor_angle))
                            output = [stick_val, 0, 0]	#[left, forward, right]
                            training_data.append([img, output])

                # right trigger pressed (motor forward)
                if controller['rt'] != 0:
                    trigger_val = round(controller['rt'], 1)
                    mapped_trigger_value = int(map_value(trigger_val, 0, 1, 133, 0))
                    if mapped_trigger_value != motor_angle:
                        motor_angle = mapped_trigger_value
                        print("F({}%) - S: {}, M: {}".format(trigger_val*100, steering_angle, motor_angle))
                        output = [0,trigger_val,0]	#[left, forward, right]
                        training_data.append([img, output])

								
                # left stick released (steering)
                if (controller['lx'] == 0) and (steering_angle != 90):
                    steering_angle = 90
                    print("ST S: {}, M: {} - Released".format(steering_angle, motor_angle))
						

                # right trigger released (motor)
                if (controller['rt'] == 0) and (motor_angle != 133):
                    motor_angle = 133
                    print("RT - S: {}, M: {} - Released".format(steering_angle, motor_angle))
						
						
                if controller['square']:
                    #print(training_data)
                    cv2.imshow("Frame", img)
                    key = cv2.waitKey(1) & 0xFF
                    #print("steering: {}, motor: {}".format(steering_angle, motor_angle))

					
    except IOError:
        print('Waiting for controller...')
        sleep(1)

		