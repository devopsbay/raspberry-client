from nfcclient.nfc_reader.nfc_read_strategy import BasicReadStrategy, RefreshingReadStrategy
from nfcclient.settings import settings


def test_basic_read_strategy(mocker, nfc_reader_impl):
    mocker.patch("adafruit_pn532.spi.PN532_SPI.read_passive_target", return_value=[12, 21, 39, 22])
    strategy = BasicReadStrategy()
    assert strategy.read_card(nfc_reader=nfc_reader_impl) == [12, 21, 39, 22]


def test_refreshing_read_strategy_called(mocker, nfc_reader_impl):
    mocker.patch("adafruit_pn532.spi.PN532_SPI.read_passive_target", return_value=[12, 21, 39, 22])
    mocker.spy(nfc_reader_impl, "reset")
    settings.NFC_REFRESHING_FEATURE_READ_MAX = 2
    strategy = RefreshingReadStrategy()

    strategy.read_card(nfc_reader=nfc_reader_impl)
    strategy.read_card(nfc_reader=nfc_reader_impl)
    strategy.read_card(nfc_reader=nfc_reader_impl)

    nfc_reader_impl.reset.assert_called_once()


def test_refreshing_read_strategy_not_called(mocker, nfc_reader_impl):
    mocker.patch("adafruit_pn532.spi.PN532_SPI.read_passive_target", return_value=[12, 21, 39, 22])
    mocker.spy(nfc_reader_impl, "reset")
    settings.NFC_REFRESHING_FEATURE_READ_MAX = 2
    strategy = RefreshingReadStrategy()

    strategy.read_card(nfc_reader=nfc_reader_impl)
    strategy.read_card(nfc_reader=nfc_reader_impl)

    nfc_reader_impl.reset.assert_not_called()
