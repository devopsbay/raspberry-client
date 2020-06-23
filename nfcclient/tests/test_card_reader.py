import pytest

from nfcclient.card_reader import authorize, read_card
from nfcclient.hub_client import AuthUser
from nfcclient.nfc_reader.nfc_reader_mock import NFCReaderMock


@pytest.mark.asyncio
def test_authorize_by_card(event_loop, requests_mock, caplog, config):
    card_id = "1"
    requests_mock.get(f"http://localhost:8123/auth/card/1/103", json={"status": True})

    assert event_loop.run_until_complete(authorize(config=config, user=AuthUser(status=True), card_id=card_id)) is True
    assert f"{card_id} Used" in caplog.text


@pytest.mark.asyncio
def test_authorize_by_master_card(event_loop, caplog, config):
    card_id = "0xda0x130x640x1a"

    assert event_loop.run_until_complete(authorize(config=config, user=AuthUser(status=True), card_id=card_id)) is True
    assert f"Master Card {card_id} Used" in caplog.text


@pytest.mark.asyncio
def test_not_authorized_by_card(event_loop, requests_mock, caplog, config):
    card_id = "1"
    door_name = "103"
    requests_mock.get(f"http://localhost:8123/auth/card/{card_id}/{door_name}", json={"status": False})

    assert event_loop.run_until_complete(
        authorize(config=config, user=AuthUser(status=False), card_id=card_id)
    ) is False
    assert f"Unauthorized Card {card_id}" in caplog.text


@pytest.mark.asyncio
def test_card_read(event_loop, mocker, config, gpio):
    door_name = "103"
    mocker.patch("nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock.read_card", return_value=[43, 21, 39, 12])
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    mocker.patch("nfcclient.card_reader.notify")
    mocker.patch("nfcclient.card_reader.authorize", return_value=True)
    nfc_reader_mock = NFCReaderMock(pin="1", door=door_name, reader_timeout=0.5)
    event_loop.run_until_complete(read_card(config=config, reader=nfc_reader_mock))

    gpio.open_door.assert_called_once_with(door_name)


@pytest.mark.asyncio
def test_card_read_not_found(event_loop, mocker, config, gpio):
    door_name = "103"
    mocker.patch("nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock.read_card", return_value=None)
    mocker.patch("nfcclient.gpio_client.GPIOClient.open_door")
    mocker.patch("nfcclient.card_reader.notify")
    mocker.patch("nfcclient.card_reader.authorize", return_value=True)
    nfc_reader_mock = NFCReaderMock(pin="1", door=door_name, reader_timeout=0.5)
    event_loop.run_until_complete(read_card(config=config, reader=nfc_reader_mock))

    gpio.open_door.assert_not_called()
