import asyncio
import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    import os
    import sys

    import fake_rpi
    from fake_rpi.RPi import GPIO
    os.environ["BLINKA_FORCEBOARD"] = 'RASPBERRY_PI_4B'
    os.environ["BLINKA_FORCECHIP"] = 'BCM2XXX'
    sys.modules["RPi"] = fake_rpi.RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO


class GPIOClient:
    def __init__(self, door_open_seconds: int = 5) -> None:
        self.doors = {}
        self.door_open_seconds = door_open_seconds

    def configure(self, doors, door_open_seconds: int = 5):
        self.door_open_seconds = door_open_seconds

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for door in doors:
            GPIO.setup(door.pin_id, GPIO.OUT)
            GPIO.output(door.pin_id, GPIO.LOW)
            self.doors[door.name] = door.pin_id

    async def open_door(self, door_name: str, seconds: int = None) -> None:
        try:
            pin = self.doors[door_name]

            if not seconds:
                seconds = self.door_open_seconds

            logging.info(f"Door {door_name} OPEN")
            GPIO.output(pin, GPIO.HIGH)
            await asyncio.sleep(seconds)
            GPIO.output(pin, GPIO.LOW)
            logging.info(f"Door {door_name} Closed")
        except KeyError:
            logging.critical(f"No door with name: {door_name}")
