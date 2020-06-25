import logging
from typing import Dict, List

from nfcclient.doors.model import Door


class DoorManager:
    _doors: Dict[str, Door]

    def __init__(self):
        self._doors = {}

    def configure(self, doors):
        self._doors.clear()
        for door in doors:
            self._doors[door.name] = Door(name=door.name, pin=door.pin_id)

    def get(self, name):
        try:
            return self._doors[name]

        except KeyError:
            logging.critical(f"No door with name: {name}")

    def all(self) -> List[Door]:
        return [door for door in self._doors.values()]


door_manager = DoorManager()
