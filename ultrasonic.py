"""ultrasonic.py

Example:
    to use as a module
    'import ultrasonic'
    or
    to view processed stream
    '$ python3 ultrasonic.py'
"""

import RPi.GPIO as GPIO
from time import sleep, time
from threading import Thread
import logging


class Ultrasonic(Thread):
    """
    Setup and use ultrasonic distance sensor to measure distance in cm

    code modified from: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
    into a module with threading
    """

    def __init__(self, thread_id, thread_name, trig_pin, echo_pin):
        """Setup GPIO pins to use ultrasonic sensor

        Args:
            thread_id (int): id of thread
            thread_name (str): name of thread
            trig_pin (int): set trigger pin of ultrasonic sensor
            echo_pin (int): set echo pin of ultrasonic sensor
        """
        logging.info('Ultrasonic: __init__')
        super(Ultrasonic, self).__init__()
        self.thread_id = thread_id
        self.name = thread_name
        self.trig = trig_pin
        self.echo = echo_pin
        self.pulse_start = 0
        self.pulse_end = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def start(self):
        """Start the thread's activity of measure method"""
        logging.info('start')
        Thread(target=self.measure(), args=()).start()
        return self

    def measure(self):
        """Measure distance from ultrasonic sensor

        Returns:
            distance (float): measured distance in cm
        """
        GPIO.output(self.trig, GPIO.LOW)
        sleep(0.1)
        GPIO.output(self.trig, GPIO.HIGH)
        sleep(0.00001)  # 10 uS delay
        GPIO.output(self.trig, GPIO.LOW)

        while GPIO.input(self.echo) == GPIO.LOW:
            self.pulse_start = time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            self.pulse_end = time()
        pulse_duration = self.pulse_end - self.pulse_start
        distance = pulse_duration * 17160.5
        distance = round(distance, 2)
        return distance


# for logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


def main():
    try:
        sensor = Ultrasonic(1, "Ultrasonic", 23, 24)
        sensor.start()
        for x in range(0, 5):
            print(sensor.measure(), "cm")

    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')

    finally:
        GPIO.cleanup()  # cleanup GPIO ports after use
        logging.info('Exiting')
        exit()


if __name__ == '__main__':
    main()
