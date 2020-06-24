import asyncio
import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO


class GPIOClient:
    def __init__(self) -> None:
        self.doors = {}
        self.door_open_seconds = 5

    def configure(self, doors, door_open_seconds: int = 5):
        self.door_open_seconds = door_open_seconds

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for door in doors:
            GPIO.setup(door.pin_id, GPIO.OUT)
            GPIO.output(door.pin_id, GPIO.LOW)
            self.doors[door.name] = {
                "pin": door.pin_id,
                "remotely_opened": False,
            }

    async def open_door(self, door_name: str, seconds: int = None, is_remote: bool = False) -> None:
        try:
            door = self.doors[door_name]
            pin = door["pin"]

            await self._open_door(door_name, pin)

            if not seconds:
                seconds = self.door_open_seconds

            if not door["remotely_opened"]:
                if is_remote:
                    door["remotely_opened"] = True
                await asyncio.sleep(seconds)
                await self._close_door(door_name, pin)
                door["remotely_opened"] = False

        except KeyError:
            logging.critical(f"No door with name: {door_name}")

    async def _open_door(self, door_name, pin):
        logging.info(f"Door {door_name} OPEN")
        GPIO.output(pin, GPIO.HIGH)

    async def _close_door(self, door_name, pin):
        GPIO.output(pin, GPIO.LOW)
        logging.info(f"Door {door_name} Closed")


gpio_client = GPIOClient()
