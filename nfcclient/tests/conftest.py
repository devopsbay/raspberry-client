import logging

import pytest
from aiohttp import web

from nfcclient import hub_client
from nfcclient.config import ClientConfig, hub_client, Door
from nfcclient.gpio_client import gpio_client
from nfcclient.doors.manager import door_manager as dm
from nfcclient.nfc_reader.nfc_reader import NFCReaderImpl
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory
from nfcclient.nfc_reader.nfc_reader_manager import NFCReaderManager
from nfcclient.router import routes
from nfcclient.settings import settings

settings.HUB_HOST_URL = "http://localhost:8123"
settings.NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock"
settings.READ_PERIOD = 0

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]}]",
    )
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")
    hub_client.hub_host = settings.HUB_HOST_URL

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
    dm.configure([Door(name="100", pin_id=21, readers=[])])
    return dm


@pytest.fixture
def nfc_reader_manager():
    NFCReaderFactory._class = None
    settings.NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock"
    return NFCReaderManager()


@pytest.fixture
def nfc_reader_patched(mocker):
    mocker.patch("busio.SPI.__init__", return_value=None)
    mocker.patch("adafruit_pn532.spi.PN532_SPI.__init__", return_value=None)
    mocker.patch("adafruit_pn532.spi.PN532_SPI.SAM_configuration", return_value=None)
    mocker.patch("adafruit_pn532.spi.PN532_SPI.get_firmware_version", return_value=[1, 2, 3, 4])


@pytest.fixture
def nfc_reader_impl(nfc_reader_patched):
    return NFCReaderImpl(pin="D2", door="120", reader_timeout=1)
