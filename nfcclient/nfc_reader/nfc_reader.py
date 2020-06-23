import logging
from typing import List

import board
import busio
from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut

from nfcclient.nfc_reader.nfc_reader_factory import NFCReader


class NFCReaderImpl(NFCReader):
    def __init__(self, pin: str, door: str, reader_timeout: float, debug: bool = False) -> None:
        super().__init__(pin=pin, door=door, reader_timeout=reader_timeout, debug=debug)
        self.pin = DigitalInOut(getattr(board, pin))

        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.PN532_SPI = PN532_SPI(spi, self.pin, debug=debug)
        self.PN532_SPI.SAM_configuration()
        ic1, ver1, rev1, support1 = self.PN532_SPI.get_firmware_version()
        logging.debug(f'Found PN532 for {self.pin._pin} with firmware version: {ver1}.{rev1}')

    def read_card(self) -> List[int]:
        uid = self.PN532_SPI.read_passive_target(timeout=self.reader_timeout)
        if uid:
            logging.info(f'Door {self.door}:{self.pin._pin} : Found card with UID: {"".join([hex(i) for i in uid])}')
            return uid
