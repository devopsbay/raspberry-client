import logging
from typing import Dict, List

from nfcclient.nfc_reader.nfc_reader import NFCReader
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory
from nfcclient.settings import settings


class NFCReaderManager:
    _nfc_readers: Dict[str, NFCReader]

    def __init__(self):
        self._nfc_readers = {}

    def configure(self, doors):
        self._nfc_readers.clear()
        for door in doors:
            for reader_pin_id in door.readers:
                try:
                    nfc_reader = NFCReaderFactory.create(
                        pin=reader_pin_id,
                        door=door.name,
                        reader_timeout=settings.READER_TIMEOUT,
                        debug=settings.DEBUG,
                    )
                    self._nfc_readers[reader_pin_id] = nfc_reader
                    logging.info(f'NFC Reader {reader_pin_id} for door {door.name} initialised')
                except Exception as e:
                    logging.critical(f'NFC Reader {reader_pin_id} for door {door.name} failed: {e}')

    def all(self) -> List[NFCReader]:
        return [reader for reader in self._nfc_readers.values()]


nfc_reader_manager = NFCReaderManager()
