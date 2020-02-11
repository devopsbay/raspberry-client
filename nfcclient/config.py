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
    doors: dict
    reader_timeout: float
    hub_host: str
    debug: bool
    # SPI connection:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

    @classmethod
    def from_env(cls):
        master_keys = list(get_env_var('MASTER_KEYS', "'0x2b0x150x270xc', '0xda0x130x640x1a', '0xca0xbf0x570x1a'"))
        doors = json.loads(os.environ.get('DOORS', '[{"name":"101","readers":["D23","D24"]},{"name":"103","readers":["D25","D26"]}]'))
        reader_timeout = float(get_env_var('READER_TIMEOUT', '0.5'))
        hub_host = get_env_var('HUB_HOST', 'http://devopsbay-alb-313417205.eu-west-1.elb.amazonaws.com')
        debug = bool(get_env_var('DEBUG_MODE', 'false'))
        return cls(master_keys=master_keys, doors=doors, reader_timeout=reader_timeout, hub_host=hub_host, debug=debug)
