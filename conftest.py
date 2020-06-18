import logging

import pytest

from nfcclient.config import ClientConfig

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)


@pytest.fixture
def config(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("HUB_HOST", "http://localhost:8123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]}]",
    )
    monkeypatch.setenv("READER_TIMEOUT", "0.5")
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")
    monkeypatch.setenv("DEBUG_MODE", "True")

    return ClientConfig.from_env()
