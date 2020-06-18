import pytest
from aiohttp import web


@pytest.fixture
def aiohttp_app(config):
    from nfcclient.api import routes
    app = web.Application()
    app.add_routes(routes)
    app["config"] = config
    return app


@pytest.fixture
def cli(loop, aiohttp_client, aiohttp_app):
    return loop.run_until_complete(aiohttp_client(aiohttp_app))


@pytest.mark.asyncio
async def test_api_refresh(cli, config, requests_mock):
    assert config.doors[0].name == "103"
    requests_mock.get("http://localhost:8123/config/1123", json={
        "master_keys": ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"],
        "doors": [
            {"name": "100", "pin_id": 21, "readers": ["D23", "D24"]},
        ],
        "reader_timeout": 0.5,
        "door_open_seconds": 1,
    })
    response = await cli.get("/refresh/")
    assert response.status == 200
    assert config.doors[0].name == "100"


@pytest.mark.asyncio
async def test_api_door_open(cli, aiohttp_app, mocker):
    aiohttp_app["config"].gpio_client.door_open_seconds = 5
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    response = await cli.get("/doors/103/open/?seconds=0")
    assert response.status == 200
    aiohttp_app["config"].gpio_client.open_door.assert_called_once_with(door_name="103", card_id="HUB", seconds=0)


@pytest.mark.asyncio
async def test_api_door_open_default_seconds(cli, aiohttp_app, mocker):
    aiohttp_app["config"].gpio_client.door_open_seconds = 0
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    response = await cli.get("/doors/103/open/")
    assert response.status == 200
    aiohttp_app["config"].gpio_client.open_door.assert_called_once_with(door_name="103", card_id="HUB", seconds=0)
