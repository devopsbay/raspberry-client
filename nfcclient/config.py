import json

import os
from dataclasses import dataclass, field

import board
import busio



class ConfigError(Exception):
    def __init__(self, field):
        super().__init__('Missing environment variable %s' % field)


def get_env_var(name: str, prefix='', allow_empty=False):
    if prefix:
        env = prefix + '_' + name
    else:
        env = name

    value = os.getenv(env)
    if not allow_empty and not value:
        raise ConfigError(env)

    return value


@dataclass(init=True)
class ClientConfig:
    master_keys: list
    doors: list
    reader_timeout: float
    hub_host: str
    debug: bool = field(default=False)
    # SPI connection:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

    @classmethod
    def from_env(cls):
        master_keys = json.loads(get_env_var('MASTER_KEYS'))
        doors = json.loads(os.environ.get('DOORS'))
        reader_timeout = float(get_env_var('READER_TIMEOUT'))
        hub_host = get_env_var('HUB_HOST')
        debug = bool(get_env_var('DEBUG_MODE', allow_empty=True))
        return cls(master_keys=master_keys, doors=doors, reader_timeout=reader_timeout, hub_host=hub_host, debug=debug)
