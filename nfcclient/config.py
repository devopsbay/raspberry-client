import json
from dataclasses import dataclass
from typing import List

from nfcclient.doors.manager import door_manager
from nfcclient.hub_client import hub_client
from nfcclient.nfc_reader.nfc_reader_manager import nfc_reader_manager
from nfcclient.settings import settings
from nfcclient.utils import get_env_var, set_env_var


@dataclass
class Door:
    name: str
    pin_id: int
    readers: List[str]

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)


@dataclass(init=True)
class ClientConfig:
    master_keys: List[str]
    door_open_seconds: int

    @classmethod
    def from_env(cls):
        doors = [
            Door(
                name=door["name"],
                pin_id=door["pin_id"],
                readers=door["readers"],
            ) for door in json.loads(get_env_var('DOORS'))
        ]
        door_manager.configure(doors=doors)
        nfc_reader_manager.configure(doors=doors)
        return cls(
            master_keys=json.loads(get_env_var('MASTER_KEYS')),
            door_open_seconds=int(get_env_var('DOOR_OPEN_SECONDS')),
        )

    def refresh_from_server(self) -> None:
        config = hub_client.get_config(settings.CLIENT_ID)
        self.master_keys = config.get("master_keys")
        self.door_open_seconds = config.get("door_open_seconds")
        doors = [Door(
            name=door["name"],
            pin_id=door["pin_id"],
            readers=door["readers"],
        ) for door in config.get("doors")]
        door_manager.configure(doors=doors)
        nfc_reader_manager.configure(doors=doors)
        set_env_var("DOOR_OPEN_SECONDS", str(self.door_open_seconds))
        set_env_var("MASTER_KEYS", self.master_keys)
        set_env_var("DOORS", config.get("doors"))
