import itertools
import logging
from time import sleep

from nfcclient.nfc_reader.nfc_read_strategy import ReadStrategy, RefreshingReadStrategy
from nfcclient.nfc_reader.nfc_reader import NFCReader
from nfcclient.settings import settings


class NFCReaderMock(NFCReader):
    def __init__(self, pin: str, door: str, reader_timeout: float, debug: bool = False) -> None:
        super().__init__(pin=pin, door=door, reader_timeout=reader_timeout, debug=debug)
        self.read_strategy = RefreshingReadStrategy(basic_read_strategy=MockReadStrategy())

    def read_card(self):
        return self.read_strategy.read_card(nfc_reader=self)

    async def reset(self):  # pragma: no cover
        self.busy = True
        logging.info(f"RESET PERFORMED {self.door}:{self.pin_number}")
        self.busy = False


class MockReadStrategy(ReadStrategy):
    cycle = itertools.cycle([None] * 9 + [[43, 21, 39, 12]])

    def read_card(self, nfc_reader):
        sleep(settings.READER_TIMEOUT)
        return next(self.cycle)
