import RPi.GPIO as GPIO
from time import sleep, time
from threading import Thread
import logging


class Ultrasonic(Thread):
    def __init__(self, thread_id, name, trig_pin, echo_pin):
        logging.info('__init__')
        super(Ultrasonic, self).__init__()
        self.thread_id = thread_id
        self.name = name
        self.trig = trig_pin
        self.echo = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def start(self):
        logging.info('start')
        Thread(target=self.measure(), args=()).start()
        return self

    def measure(self):
        # logging.info('measure')
        GPIO.output(self.trig, GPIO.LOW)
        sleep(0.1)
        GPIO.output(self.trig, GPIO.HIGH)
        sleep(0.00001)  # 10 uS delay
        GPIO.output(self.trig, GPIO.LOW)

        while GPIO.input(self.echo) == GPIO.LOW:
            pulse_start = time()
        while GPIO.input(self.echo) == GPIO.HIGH:
            pulse_end = time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17160.5
        distance = round(distance, 2)
        return distance


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
