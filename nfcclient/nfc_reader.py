import logging

from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut
import board


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
        print('Found PN532 with firmware version: {0}.{1}'.format(ver1, rev1))

    @staticmethod
    def read_uid(uid):
        return [hex(i) for i in uid]

    def _read_passive_target_(self):
        uid = self.PN532_SPI.read_passive_target(timeout=self.reader_timeout)
        logging.info('{}: \nFound card with UID:'.format(self.door), self.read_uid(uid))
        return uid

    def read_card(self):
        uid = self._read_passive_target_()
        return self.read_uid(uid)
