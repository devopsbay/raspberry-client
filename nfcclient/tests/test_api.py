import pytest

from nfcclient.config import ClientConfig


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_api_door_open(cli, aiohttp_app, mocker, gpio):
    gpio.door_open_seconds = 5
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    response = await cli.get("/doors/103/open/?seconds=0")
    assert response.status == 200
    gpio.open_door.assert_called_once_with(door_name="103", seconds=0)


@pytest.mark.asyncio
async def test_api_door_open_default_seconds(cli, aiohttp_app, mocker, gpio):
    gpio.door_open_seconds = 0
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    response = await cli.get("/doors/103/open/")
    assert response.status == 200
    gpio.open_door.assert_called_once_with(door_name="103", seconds=0)
