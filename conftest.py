import logging

import pytest
from aiohttp import web

from nfcclient import hub_client
from nfcclient.gpio_client import gpio_client
from nfcclient.doors.manager import door_manager as dm
from nfcclient.router import routes

HUB_CLIENT = "http://localhost:8123"
hub_client.hub_client = hub_client.HubClient(HUB_CLIENT)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)


@pytest.fixture
def hub_client_url():
    return HUB_CLIENT


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]}]",
    )
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")

    from nfcclient.config import ClientConfig
    return ClientConfig.from_env()


@pytest.fixture
def aiohttp_app(config):
    app = web.Application()
    app["config"] = config
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    return app


@pytest.fixture
def cli(loop, aiohttp_client, aiohttp_app):
    return loop.run_until_complete(aiohttp_client(aiohttp_app))


@pytest.fixture
def gpio():
    return gpio_client


@pytest.fixture
def door_manager():
    dm.configure([{"name": "100", "pin_id": 21}])
    return dm
