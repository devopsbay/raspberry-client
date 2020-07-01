import asyncio

import pytest

from nfcclient.doors.model import Door

pytestmark = pytest.mark.asyncio


def test_open_door(event_loop, mocker):
    door = Door(name="103", pin=20)
    mocker.spy(door, "_open")
    event_loop.run_until_complete(door.open(seconds=1))
    door._open.assert_called_once()
    assert door._closing_task is not None


async def test_open_door_0_seconds_closes_door(event_loop, mocker):
    door = Door(name="103", pin=20)
    mocker.spy(door, "_open")
    mocker.spy(door, "_close")
    tasks = [
        event_loop.create_task(door.open(seconds=1)),
        event_loop.create_task(door.open(seconds=0)),
    ]
    await asyncio.gather(*tasks)

    door._open.assert_called_once()
    assert door._opened is False
    door._close.assert_called_once()
    assert door._closing_task is None


async def test_open_door_with_remote_precedent(event_loop, mocker):
    door = Door(name="103", pin=20)
    mocker.spy(door, "_open")
    mocker.spy(door, "_cancel_closing_doors")
    tasks = [
        event_loop.create_task(door.open(seconds=1)),
        event_loop.create_task(door.open(seconds=2, remote=True)),
    ]
    await asyncio.gather(*tasks)

    door._open.assert_called_once()
    door._cancel_closing_doors.assert_called_once()
