import RPi.GPIO as GPIO
import time


class Servo:
    PIN = 12
    ORIGIN = 12

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(self.PIN, 50)
        self.pwm.start(self.ORIGIN)

    def set_position(degree):
        if degree < 0 and degree > 180:
            print("Value must be between 0° and 180°.")
        else:
            position = degree / 360 * 10 + 2
            self.pwm.ChangeDutyCycle(position)
            time.sleep(0.5)  # Time needed to reach position

    def shutdown(self):
        self.pwm.stop()
        GPIO.cleanup()
