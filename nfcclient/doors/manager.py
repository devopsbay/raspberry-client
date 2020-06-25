import logging
from typing import Dict

from nfcclient.doors.model import Door


class DoorManager:
    _doors: Dict[str, Door]

    def __init__(self):
        self._doors = {}

    def configure(self, doors):
        self._doors.clear()
        for door in doors:
            self._doors[door["name"]] = Door(name=door["name"], pin=door["pin_id"])

    def get(self, name):
        try:
            door = self._doors[name]
            return door

        except KeyError:
            logging.critical(f"No door with name: {name}")


door_manager = DoorManager()
