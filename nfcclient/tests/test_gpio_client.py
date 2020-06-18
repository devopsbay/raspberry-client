import asyncio

import pytest

from nfcclient.config import Door
from nfcclient.gpio_client import GPIOClient


@pytest.mark.asyncio
def test_open_door(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=0)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    event_loop.run_until_complete(gpio_client.open_door("103", "1"))
    assert "Door 103 OPEN for 1" in caplog.text
    assert "Door 103 Closed" in caplog.text


@pytest.mark.asyncio
def test_open_door_failed(caplog, event_loop):
    gpio_client = GPIOClient(door_open_seconds=0)
    gpio_client.configure([Door(name="103", pin_id=21, readers=["D23", "D24"])])
    event_loop.run_until_complete(gpio_client.open_door("100", "1"))
    assert "No door with name: 100" in caplog.text
