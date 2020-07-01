import pytest

from nfcclient.nfc_reader.nfc_read_strategy import BasicReadStrategy, RefreshingReadStrategy
from nfcclient.nfc_reader.nfc_reader import NFCReader, NFCReaderImpl
from nfcclient.settings import settings


def test_nfc_reader_is_abstract():
    with pytest.raises(NotImplementedError):
        NFCReader("1", "1", 10).read_card()


def test_read_card(mocker, nfc_reader_impl):
    mocker.patch("adafruit_pn532.spi.PN532_SPI.read_passive_target", return_value=[43, 21, 39, 12])
    assert nfc_reader_impl.read_card() == [43, 21, 39, 12]


def test_read_card_empty(mocker, nfc_reader_impl):
    mocker.patch("adafruit_pn532.spi.PN532_SPI.read_passive_target", return_value=None)
    assert nfc_reader_impl.read_card() is None


def test_default_strategy_used(nfc_reader_patched):
    settings.NFC_REFRESHING_FEATURE = False
    reader = NFCReaderImpl(pin="D2", door="101", reader_timeout=1)

    assert isinstance(reader.read_strategy, BasicReadStrategy)


def test_refreshing_strategy_used(nfc_reader_patched):
    settings.NFC_REFRESHING_FEATURE = True
    reader = NFCReaderImpl(pin="D2", door="101", reader_timeout=1)

    assert isinstance(reader.read_strategy, RefreshingReadStrategy)
