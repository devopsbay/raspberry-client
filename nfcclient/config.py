import json
import os
from dataclasses import dataclass, field
from typing import List

from nfcclient.gpio_client import GPIOClient
from nfcclient.hub_client import HubClient


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
    _class = None

    client_id: str
    hub_client: HubClient
    gpio_client: GPIOClient
    master_keys: List[str]
    doors: List[Door]
    reader_timeout: float
    debug: bool = field(default=False)

    @classmethod
    def from_env(cls):
        if cls._class:
            return cls._class

        gpio_client = GPIOClient()
        doors = [Door(
            name=door["name"],
            pin_id=door["pin_id"],
            readers=door["readers"],
        ) for door in json.loads(os.environ.get('DOORS'))]
        gpio_client.configure(
            doors=doors,
            door_open_seconds=int(get_env_var('DOOR_OPEN_SECONDS')),
        )
        return cls(
            client_id=get_env_var('CLIENT_ID'),
            hub_client=HubClient(get_env_var('HUB_HOST')),
            gpio_client=gpio_client,
            master_keys=json.loads(get_env_var('MASTER_KEYS')),
            doors=doors,
            reader_timeout=float(get_env_var('READER_TIMEOUT')),
            debug=bool(get_env_var('DEBUG_MODE', allow_empty=True)),
        )

    def refresh_from_server(self) -> None:
        config = self.hub_client.get_config(self.client_id)
        self.master_keys = config.get("master_keys")
        self.doors = [Door(
            name=door["name"],
            pin_id=door["pin_id"],
            readers=door["readers"],
        ) for door in config.get("doors")]
        self.reader_timeout = config.get("reader_timeout")
        self.debug = config.get("debug")
        self.gpio_client.configure(
            doors=self.doors,
            door_open_seconds=config.get("door_open_seconds"),
        )
