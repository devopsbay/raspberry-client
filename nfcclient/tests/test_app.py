import pytest

from nfcclient.app import client_app

pytestmark = pytest.mark.asyncio


async def test_stop_on_exception(mocker, config):
    mocker.patch("nfcclient.card_reader.read_card")
    mocker.patch("nfcclient.nfc_reader.nfc_reader_manager.NFCReaderManager.all").side_effect = Exception("LOL")
    with pytest.raises(Exception):
        await client_app(client_config=config)


async def test_clean(mocker, config):
    mocker.patch("nfcclient.card_reader.read_card")
    mocker.patch("nfcclient.nfc_reader.nfc_reader_manager.NFCReaderManager.all").side_effect = Exception("LOL")
    mocker.spy(config, "clean")
    with pytest.raises(Exception):
        await client_app(client_config=config)
        config.clean.assert_called_once()


async def test_doesnt_stop_on_runtime_error(mocker, config, nfc_reader_manager):
    def side_effect():
        return [RuntimeError("RuntimeError"), Exception("LOL")]

    mocker.patch("nfcclient.card_reader.read_card")
    mocker.patch("nfcclient.nfc_reader.nfc_reader_manager.NFCReaderManager.all").side_effect = side_effect()
    mocker.spy(nfc_reader_manager, "configure")
    with pytest.raises(Exception):
        await client_app(client_config=config)
        nfc_reader_manager.configure.assert_called_once()
