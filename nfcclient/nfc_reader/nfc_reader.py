import logging
from typing import List

import board
import busio
from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut

from nfcclient.nfc_reader.nfc_read_strategy import BasicReadStrategy, RefreshingReadStrategy
from nfcclient.settings import settings


class NFCReader:
    read_strategy = None

    def __init__(self, pin: str, door: str, reader_timeout: float, debug: bool = False):
        self.pin_number = pin
        self.door = door
        self.reader_timeout = reader_timeout
        self.debug = debug

    def read_card(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class NFCReaderImpl(NFCReader):
    pin = None
    spi = None
    pn532 = None

    def __init__(self, pin: str, door: str, reader_timeout: float, debug: bool = False) -> None:
        super().__init__(pin=pin, door=door, reader_timeout=reader_timeout, debug=debug)
        self._configure()

        if settings.NFC_REFRESHING_FEATURE:
            self.read_strategy = RefreshingReadStrategy(BasicReadStrategy())

        if not self.read_strategy:
            self.read_strategy = BasicReadStrategy()

    def read_card(self) -> List[int]:
        return self.read_strategy.read_card(nfc_reader=self)

    def reset(self):
        logging.info(f"NFC Reader reset {self.pin._pin}")
        self._configure()

    def _configure(self):
        self.pin = DigitalInOut(getattr(board, self.pin_number))
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.pn532 = PN532_SPI(self.spi, self.pin, debug=self.debug)
        self.pn532.SAM_configuration()
        ic1, ver1, rev1, support1 = self.pn532.get_firmware_version()
        logging.debug(f'Found PN532 for {self.pin._pin} with firmware version: {ver1}.{rev1}')
