from typing import Type

from nfcclient.nfc_reader.nfc_reader import NFCReader
from nfcclient.settings import settings


class NFCReaderFactory:
    _class = None

    @classmethod
    def _get_class(cls) -> Type[NFCReader]:
        if cls._class is None:
            nfc_reader_module = settings.NFC_READER_MODULE
            d = nfc_reader_module.rfind(".")
            classname = nfc_reader_module[d + 1:len(nfc_reader_module)]
            module = __import__(nfc_reader_module[0:d], globals(), locals(), [classname])
            cls._class = getattr(module, classname)
        return cls._class

    @classmethod
    def create(cls, pin: str, door: str, reader_timeout: float, debug: bool = False) -> NFCReader:
        return cls._get_class()(pin=pin, door=door, reader_timeout=reader_timeout, debug=debug)
