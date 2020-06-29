import json
import os

import dotenv


class ConfigError(Exception):
    def __init__(self, field):
        super().__init__(f'Missing environment variable {field}')


def get_env_var(name: str, default: str = None, prefix='', allow_empty=False):
    if prefix:
        env = prefix + '_' + name
    else:
        env = name

    value = os.getenv(env)

    if not value and default:
        value = default

    if not allow_empty and not value:
        raise ConfigError(env)

    return value


def set_env_var(name: str, value):
    if isinstance(value, (list, dict, tuple)):
        value = json.dumps(value).replace(" ", "")

    dotenv.set_key(".env", key_to_set=name, value_to_set=value, quote_mode="")
