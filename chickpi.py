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
        time.sleep(cfg["feeding_factor"])
        servo.set_position(0)
        servo.shutdown()

    def open_door(self):
        stepper = Stepmotor()
        stepper.rotate(doorheight_in_degrees())
        stepper.shutdown()

    def close_door(self):
        stepper = Stepmotor()
        stepper.rotate(-doorheight_in_degrees())
        stepper.shutdown()

    def doorheight_to_degrees(self):
        rotations = cfg["door_open_height_in_mm"] / 25.13  # Measured spool circumfence
        return rotations * 360


# Run it

chickpi = Chickpi()

schedule.every().day.at(cfg["opening_time"]).do(chickpi.open_door)
schedule.every().day.at(cfg["closing_time"]).do(chickpi.close_door)
for feeding_time in cfg["feeding_times"]:
    schedule.every().day.at(feeding_time).do(chickpi.feed)

while True:
    schedule.run_pending()
    time.sleep(60)
