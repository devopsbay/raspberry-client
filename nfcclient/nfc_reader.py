from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut
import board

from config import logger


class NFCReaderException(Exception):
    pass


class NFCReader:

    def __init__(self, config, pin, door):
        self.door = door
        self.pin = DigitalInOut(eval('board.{}'.format(pin)))
        self.reader_timeout = config.reader_timeout
        self.debug = config.debug

        self.PN532_SPI = PN532_SPI(config.spi, self.pin, debug=config.debug)
        self.PN532_SPI.SAM_configuration()
        self.firmware_version()

    def firmware_version(self):
        ic1, ver1, rev1, support1 = self.PN532_SPI.get_firmware_version()
        logger.debug('Found PN532 for {0} with firmware version: {1}.{2}'.format(str(self.pin._pin), ver1, rev1))

    @staticmethod
    def hex_uid(uid):
        return [hex(i) for i in uid]

    @staticmethod
    def str_uid(uid):
        return "".join([hex(i) for i in uid])

    def _read_passive_target_(self):
        return self.PN532_SPI.read_passive_target(timeout=self.reader_timeout)

    def read_card(self):
        uid = self._read_passive_target_()
        if uid:
            logger.info('Door {}:{} : Found card with UID: {}'.format(self.door, str(self.pin._pin), self.str_uid(uid)))
            return uid
