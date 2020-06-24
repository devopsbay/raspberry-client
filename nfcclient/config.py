import json
import os
from dataclasses import dataclass
from typing import List

from nfcclient.doors.manager import door_manager
from nfcclient.hub_client import hub_client


class ConfigError(Exception):
    def __init__(self, field):
        super().__init__(f'Missing environment variable {field}')


def get_env_var(name: str, prefix='', allow_empty=False):
    if prefix:
        env = prefix + '_' + name
    else:
        env = name

    value = os.getenv(env)
    if not allow_empty and not value:
        raise ConfigError(env)

    return value


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
    client_id: str
    master_keys: List[str]
    doors: List[Door]
    door_open_seconds: int

    @classmethod
    def from_env(cls):
        doors = json.loads(get_env_var('DOORS'))
        door_manager.configure(doors=doors)
        return cls(
            client_id=get_env_var('CLIENT_ID'),
            master_keys=json.loads(get_env_var('MASTER_KEYS')),
            doors=[Door(
                name=door["name"],
                pin_id=door["pin_id"],
                readers=door["readers"],
            ) for door in doors],
            door_open_seconds=int(get_env_var('DOOR_OPEN_SECONDS')),
        )

    def refresh_from_server(self) -> None:
        config = hub_client.get_config(self.client_id)
        self.master_keys = config.get("master_keys")
        self.doors = [Door(
            name=door["name"],
            pin_id=door["pin_id"],
            readers=door["readers"],
        ) for door in config.get("doors")]
        self.door_open_seconds = int(config.get("door_open_seconds"))
        door_manager.configure(doors=config.get("doors"))
