import pytest

from nfcclient.nfc_reader.nfc_reader import NFCReaderImpl
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory, NFCReader
from nfcclient.nfc_reader.nfc_reader_mock import NFCReaderMock


def test_nfc_reader_is_abstract():
    with pytest.raises(NotImplementedError):
        NFCReader("1", "1", 10).read_card()


def test_factory_create_mock(monkeypatch):
    monkeypatch.setenv("NFC_READER_MODULE", "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock")
    NFCReaderFactory._class = None
    nfc_reader = NFCReaderFactory.create("D23", "2", 5)
    assert type(nfc_reader) == NFCReaderMock


def test_factory_create_impl(monkeypatch, mocker):
    mocker.patch("nfcclient.nfc_reader.nfc_reader.NFCReaderImpl.__init__", return_value=None)
    monkeypatch.setenv("NFC_READER_MODULE", "nfcclient.nfc_reader.nfc_reader.NFCReaderImpl")
    NFCReaderFactory._class = None
    nfc_reader = NFCReaderFactory.create("D23", "2", 5)
    assert type(nfc_reader) == NFCReaderImpl
    NFCReaderImpl.__init__.assert_called_once_with(pin="D23", door="2", reader_timeout=5, debug=False)


def test_factory_does_not_return_same_reader(monkeypatch, mocker):
    mocker.patch("nfcclient.nfc_reader.nfc_reader.NFCReaderImpl.__init__", return_value=None)
    monkeypatch.setenv("NFC_READER_MODULE", "nfcclient.nfc_reader.nfc_reader.NFCReaderImpl")
    NFCReaderFactory._class = None
    nfc_reader_1 = NFCReaderFactory.create("D23", "2", 5)
    nfc_reader_2 = NFCReaderFactory.create("D23", "2", 5)
    assert nfc_reader_1 != nfc_reader_2
    NFCReaderImpl.__init__.assert_called_with(pin="D23", door="2", reader_timeout=5, debug=False)
