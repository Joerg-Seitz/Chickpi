import yaml
import schedule
import time
from components.mg996r_servo import Servo
from components.nema17_stepmotor import Stepmotor
from pathlib import Path

cfgpath = Path(__file__).parent / "config.yml"
with open(str(cfgpath), "r") as cfgfile:
    cfg = yaml.full_load(cfgfile)


class Chickpi(Resource):
    def feed(self):
        servo = Servo()
        servo.set_position(108)
        time.sleep(0.4)  # feeding
        servo.set_position(0)
        servo.shutdown()

    def open_door(self):
        stepper = Stepmotor()
        stepper.rotate(7200)
        stepper.shutdown()

    def close_door(self):
        stepper = Stepmotor()
        stepper.rotate(-7200)
        stepper.shutdown()


# Run it

chickpi = Chickpi()

schedule.every().day.at(cfg["opening_time"]).do(chickpi.open_door)
schedule.every().day.at(cfg["closing_time"]).do(chickpi.close_door)
for feeding_time in cfg["feeding_times"]:
    schedule.every().day.at(feeding_time).do(chickpi.feed)

while True:
    schedule.run_pending()
    time.sleep(60)
