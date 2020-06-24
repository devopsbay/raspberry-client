import pytest

from nfcclient.config import ClientConfig

pytestmark = pytest.mark.asyncio


async def test_api_refresh(cli, aiohttp_app, monkeypatch, requests_mock):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]}]",
    )
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")
    config = ClientConfig.from_env()

    assert config.doors[0].name == "103"
    requests_mock.get("http://localhost:8123/config/1123", json={
        "master_keys": ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"],
        "doors": [
            {"name": "100", "pin_id": 21, "readers": ["D23", "D24"]},
        ],
        "reader_timeout": 0.5,
        "door_open_seconds": 1,
    })

    aiohttp_app["config"] = config
    response = await cli.get("/refresh/")
    assert response.status == 200
    assert config.doors[0].name == "100"


async def test_api_door_open(cli, aiohttp_app, mocker, gpio, door_manager):
    door_manager.configure([{"name": "103", "pin_id": 20}])
    mocker.patch("nfcclient.doors.model.Door.open")
    response = await cli.get("/doors/103/open/?seconds=1")
    assert response.status == 200
    door_manager.get("103").open.assert_called_once_with(seconds=1, remote=True)
