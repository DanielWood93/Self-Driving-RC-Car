# drive rc car with xbox one controller, only used for testing

from picamera.array import PiRGBArray  # for pi camera
from picamera import PiCamera  # for pi camera
from approxeng.input.selectbinder import ControllerResource  # for xbox controller
from pca9685_driver import Device  # for PCA9685 servo driver
from time import sleep

pwm = Device(0x40)  # setup PCA9685 servo driver
pwm.set_pwm_frequency(60)  # setup PCA9685 servo driver

steering_angle = 90  # initial angle of servo for steering
motor_angle = 133  # initial angle of servo for motor


def set_angle(channel, angle):
    pulse = (int(angle) * 2.5) + 150
    pwm.set_pwm(channel, int(pulse))


print('Ready, drive only')
while 1:
    try:
        with ControllerResource(print_events=False, controller_class=None, hot_zone=0.1,
                                dead_zone=0.1) as controller:
            print('Found a controller')
            while controller.connected:
                set_angle(14, steering_angle)
                set_angle(15, motor_angle)
            
                # right trigger moved (motor forward)
                if controller['rt'] == 1:
                    motor_angle = 125
                    
                # left stick moved (steering)
                if controller['lx'] is not 0:
                    stick_val = int(controller['lx'])

                    if stick_val > 0:  # right
                        steering_angle = 60

                    if stick_val < 0:  # left
                        steering_angle = 120
        
                # left stick released (steering centered)
                if (controller['lx'] is 0) and (steering_angle is not 90):
                    steering_angle = 90

                # right trigger released (motor stopped)
                if controller['rt'] is 0:
                    motor_angle = 133

    except IOError:
        print('Waiting for controller...')
        sleep(1)
        