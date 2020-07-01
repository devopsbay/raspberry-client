from nfcclient.nfc_reader.nfc_reader import NFCReaderImpl
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory
from nfcclient.nfc_reader.nfc_reader_mock import NFCReaderMock
from nfcclient.settings import settings


def test_factory_create_mock(monkeypatch):
    NFCReaderFactory._class = None
    settings.NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock"
    nfc_reader = NFCReaderFactory.create("D23", "2", 5)
    assert type(nfc_reader) == NFCReaderMock
    assert nfc_reader.read_card() is None or [43, 21, 39, 12]


def test_factory_create_impl(mocker):
    mocker.patch("nfcclient.nfc_reader.nfc_reader.NFCReaderImpl.__init__", return_value=None)
    NFCReaderFactory._class = None
    settings.NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader.NFCReaderImpl"
    nfc_reader = NFCReaderFactory.create("D23", "2", 5)
    assert type(nfc_reader) == NFCReaderImpl
    NFCReaderImpl.__init__.assert_called_once_with(pin="D23", door="2", reader_timeout=5, debug=False)


def test_factory_does_not_return_same_reader(mocker):
    mocker.patch("nfcclient.nfc_reader.nfc_reader.NFCReaderImpl.__init__", return_value=None)
    NFCReaderFactory._class = None
    nfc_reader_1 = NFCReaderFactory.create("D23", "2", 5)
    nfc_reader_2 = NFCReaderFactory.create("D23", "2", 5)
    assert nfc_reader_1 != nfc_reader_2
    NFCReaderImpl.__init__.assert_called_with(pin="D23", door="2", reader_timeout=5, debug=False)