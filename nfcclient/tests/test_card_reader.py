import pytest

from nfcclient.card_reader import CardReaderFacade, runner
from nfcclient.config import Door, ClientConfig
from nfcclient.nfc_reader.nfc_reader_mock import NFCReaderMock

pytestmark = pytest.mark.asyncio


def test_authorize_by_card(event_loop, caplog, config):
    card_id = "1"
    reader = CardReaderFacade(config)
    assert event_loop.run_until_complete(reader.authorize(auth={"status": True}, card_id=card_id)) is True
    assert f"{card_id} Used" in caplog.text


def test_authorize_by_master_card(event_loop, caplog, config):
    card_id = "0xda0x130x640x1a"
    reader = CardReaderFacade(config)
    assert event_loop.run_until_complete(reader.authorize(auth={"status": True}, card_id=card_id)) is True
    assert f"Master Card {card_id} Used" in caplog.text


def test_not_authorized_by_card(event_loop, caplog, config):
    card_id = "1"
    reader = CardReaderFacade(config)
    assert event_loop.run_until_complete(
        reader.authorize(auth={"status": False}, card_id=card_id)
    ) is False
    assert f"Unauthorized Card {card_id}" in caplog.text


def test_card_read(event_loop, mocker, config, gpio, door_manager):
    door_name = "103"
    pin = 1
    door_manager.configure([Door(name=door_name, pin_id=pin, readers=[])])
    mocker.patch("nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock.read_card", return_value=[43, 21, 39, 12])
    mocker.patch("nfcclient.card_reader.CardReaderFacade.authorize", return_value=True)
    mocker.patch("nfcclient.doors.model.Door._open")
    nfc_reader_mock = NFCReaderMock(pin="1", door=door_name, reader_timeout=0.5)
    reader = CardReaderFacade(config)
    event_loop.run_until_complete(reader.read_card(reader=nfc_reader_mock))

    door_manager.get(door_name)._open.assert_called_once()


def test_card_read_not_found(event_loop, mocker, config, gpio):
    door_name = "103"
    mocker.patch("nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock.read_card", return_value=None)
    mocker.patch("nfcclient.gpio_client.GPIOClient.open")
    mocker.patch("nfcclient.card_reader.CardReaderFacade.authorize", return_value=True)
    nfc_reader_mock = NFCReaderMock(pin="1", door=door_name, reader_timeout=0.5)
    reader = CardReaderFacade(config)
    event_loop.run_until_complete(reader.read_card(reader=nfc_reader_mock))

    gpio.open.assert_not_called()


async def test_stop_on_exception(mocker, config):
    mocker.patch("nfcclient.card_reader.CardReaderFacade.read_card")
    mocker.patch("nfcclient.doors.manager.DoorManager.all_by_not_opened").side_effect = Exception("LOL")
    with pytest.raises(Exception):
        await runner(client_config=config)


async def test_clean(mocker, config):
    mocker.patch("nfcclient.card_reader.CardReaderFacade.read_card")
    mocker.patch("nfcclient.doors.manager.DoorManager.all_by_not_opened").side_effect = Exception("LOL")
    mocker.spy(config, "clean")
    with pytest.raises(Exception):
        await runner(client_config=config)
        config.clean.assert_called_once()


async def test_doesnt_stop_on_runtime_error(mocker, config, nfc_reader_manager):
    def side_effect():
        return [RuntimeError("RuntimeError"), Exception("LOL")]

    mocker.patch("nfcclient.card_reader.CardReaderFacade.read_card")
    mocker.patch("nfcclient.doors.manager.DoorManager.all_by_not_opened").side_effect = side_effect()
    mocker.spy(nfc_reader_manager, "configure")
    with pytest.raises(Exception):
        await runner(client_config=config)
        nfc_reader_manager.configure.assert_called_once()


async def test_read_cards_only_not_opened(monkeypatch, mocker, door_manager):
    monkeypatch.setenv("CLIENT_ID", "1123")
    monkeypatch.setenv("MASTER_KEYS", '["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]')
    monkeypatch.setenv(
        "DOORS",
        (
            "[{\"name\":\"103\",\"pin_id\":21,\"readers\":[\"D23\",\"D24\"]},"
            "{\"name\":\"104\",\"pin_id\":22,\"readers\":[\"D25\",\"D26\"]}]"
        ),
    )
    monkeypatch.setenv("DOOR_OPEN_SECONDS", "1")

    config = ClientConfig.from_env()
    door_manager.get("103")._opened = True

    mocker.spy(CardReaderFacade, "read_card")

    reader = CardReaderFacade(config)
    await reader.read_cards()

    assert reader.read_card.call_count == 2


def test_pop_finished_task(config):
    reader = CardReaderFacade(config)
    reader.tasks = {"D1": 1, "D2": 2, "D3": 3}
    reader._pop_finished_task(2)
    assert len(reader.tasks) == 2
    assert reader.tasks == {"D1": 1, "D3": 3}