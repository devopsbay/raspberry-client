import pytest
from aioresponses import aioresponses

from nfcclient.config import Door, ClientConfig
from nfcclient.settings import settings

pytestmark = pytest.mark.asyncio


def test_client_config_from_env(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]}]",
    )
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")

    config = ClientConfig.from_env()

    assert config.master_keys == ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]
    assert config.door_open_seconds == 1


async def test_client_config_refresh_from_server(monkeypatch, config):
    with aioresponses() as mocked:
        mocked.get(f"{settings.HUB_HOST_URL}/config/1", payload={
            "master_keys": ["0x2b0x150x270xc"],
            "doors": [{"name": "121", "pin_id": 22, "readers": ["D23", "D24"]}],
            "door_open_seconds": 2,
        })

        await config.refresh_from_server()

        assert config.master_keys == ["0x2b0x150x270xc"]
        assert config.door_open_seconds == 2


def test_doors():
    d = Door.from_dict({
        "name": "a",
        "pin_id": 1,
        "readers": ["b"],
    })
    assert d.name == "a"
    assert d.pin_id == 1
    assert d.readers == ["b"]


def test_clean(config, door_manager):
    door_manager.configure([
        Door(name="lol1", pin_id=22, readers=[]),
        Door(name="lol2", pin_id=23, readers=[]),
        Door(name="lol3", pin_id=24, readers=[]),
    ])
    door_manager.all()
    assert len(door_manager.all()) == 3

    config.clean()
    assert len(door_manager.all()) == 0
