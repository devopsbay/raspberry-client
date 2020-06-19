import asyncio

import pytest

from nfcclient.config import Door
from nfcclient.gpio_client import GPIOClient

pytestmark = pytest.mark.asyncio


def test_open_door(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=0)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    event_loop.run_until_complete(gpio_client.open_door("103"))
    assert "Door 103 OPEN" in caplog.text
    assert "Door 103 Closed" in caplog.text


def test_open_door_failed(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=0)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    event_loop.run_until_complete(gpio_client.open_door("100"))
    assert "No door with name: 100" in caplog.text


async def test_open_door_with_remote_precedent(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=1)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    tasks = [
        event_loop.create_task(gpio_client.open_door("103", seconds=1, is_remote=True)),
        event_loop.create_task(gpio_client.open_door("103", seconds=0)),
    ]
    await asyncio.gather(*tasks)
    assert caplog.text.count("Door 103 OPEN") == 2
    assert caplog.text.count("Door 103 Closed") == 1


async def test_open_door_without_remote_precedent(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=1)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    tasks = [
        event_loop.create_task(gpio_client.open_door("103", seconds=1)),
        event_loop.create_task(gpio_client.open_door("103", seconds=0)),
    ]
    await asyncio.gather(*tasks)
    assert caplog.text.count("Door 103 OPEN") == 2
    assert caplog.text.count("Door 103 Closed") == 2
