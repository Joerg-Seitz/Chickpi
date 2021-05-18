import RPi.GPIO as GPIO
import time


class Stepmotor:
    STEPS_PER_ROTATION = 100.0
    CLOCKWISE_SEQUENCE = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]
    PIN_1 = 29
    PIN_2 = 31
    PIN_3 = 33
    PIN_4 = 35

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_1, GPIO.OUT)
        GPIO.setup(self.PIN_2, GPIO.OUT)
        GPIO.setup(self.PIN_3, GPIO.OUT)
        GPIO.setup(self.PIN_4, GPIO.OUT)

    def set_pins(self, v1, v2, v3, v4):
        GPIO.output(self.PIN_1, v1)
        GPIO.output(self.PIN_2, v2)
        GPIO.output(self.PIN_3, v3)
        GPIO.output(self.PIN_4, v4)
        time.sleep(0.002)  # Time needed to reach position

    def step(self, sequence):
        for signals in sequence:
            self.set_pins(*signals)

    def rotate(self, degrees):
        steps = self.STEPS_PER_ROTATION / 360 * abs(degrees)
        sequence = (
            self.CLOCKWISE_SEQUENCE
            if degrees > 0
            else list(reversed(self.CLOCKWISE_SEQUENCE))
        )
        while steps > 0.0:
            self.step(sequence)
            steps -= 1

    def shutdown(self):
        self.set_pins(0, 0, 0, 0)
        GPIO.cleanup()
