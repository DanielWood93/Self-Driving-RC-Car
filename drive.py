from pca9685_driver import Device  # for PCA9685 servo driver
import time


class Drive:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        self.pwm = Device(0x40)  # setup PCA9685 servo driver device
        self.pwm.set_pwm_frequency(60)  # setup PCA9685 servo driver frequency
        self.steering_angle = 90  # set initial angle of servo for steering
        self.motor_angle = 133  # set initial angle of servo for motor
        self.set_angle(14, self.steering_angle)  # set angle for motors
        self.set_angle(15, self.motor_angle)  # set angle for motors


    def set_angle(self, channel, angle):
        """Calculate pulse width and set angle of servo motor
        Args:
            channel: channel of servo motor which is to be changed
            angle: angle to set servo motor to
        """
        pulse = (int(angle) * 2.5) + 150
        self.pwm.set_pwm(channel, int(pulse))

    def car_stopped(self):
        self.steering_angle = 90
        self.motor_angle = 133
        self.set_angle(14, self.steering_angle)  # set angle for motors
        self.set_angle(15, self.motor_angle)  # set angle for motors

    def drive_forward(self):
        self.steering_angle = 90
        self.motor_angle = 125
        self.set_angle(14, self.steering_angle)  # set angle for motors
        self.set_angle(15, self.motor_angle)  # set angle for motors

    def drive_left(self):
        self.steering_angle = 120
        self.motor_angle = 125
        self.set_angle(14, self.steering_angle)  # set angle for motors
        self.set_angle(15, self.motor_angle)  # set angle for motors

    def drive_right(self):
        self.steering_angle = 60
        self.motor_angle = 125
        self.set_angle(14, self.steering_angle)  # set angle for motors
        self.set_angle(15, self.motor_angle)  # set angle for motors


def main():
    car = Drive(1, 'DataCapture')

    print("Left")
    car.drive_left()
    time.sleep(2)

    print("Forward")
    car.drive_forward()
    time.sleep(2)

    print("Right")
    car.drive_right()
    time.sleep(2)

    print("Stopped")
    car.car_stopped()
    time.sleep(2)

    exit()


if __name__ == '__main__':
    main()