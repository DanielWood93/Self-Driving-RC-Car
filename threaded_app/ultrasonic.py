import RPi.GPIO as GPIO
from time import sleep, time


class Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        self.trig = trig_pin
        self.echo = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def measure(self):
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


def main():
    try:
        sensor = Ultrasonic(23, 24)
        for x in range(0, 5):
            print(sensor.measure(), "cm")
    finally:
        GPIO.cleanup()  # cleanup GPIO ports after use


if __name__ == '__main__':
    main()
