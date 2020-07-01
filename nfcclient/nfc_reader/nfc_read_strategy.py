import logging

from nfcclient.settings import settings


class BasicReadStrategy:
    def read_card(self, nfc_reader):
        uid = nfc_reader.PN532_SPI.read_passive_target(timeout=nfc_reader.reader_timeout)
        if uid:
            logging.info(
                f'Door {nfc_reader.door}:{nfc_reader.pin._pin} : Found card with UID: {"".join([hex(i) for i in uid])}'
            )
            return uid


class RefreshingReadStrategy(BasicReadStrategy):
    _reset_count: int = 0

    def read_card(self, nfc_reader):
        if self._reset_count == settings.NFC_REFRESHING_FEATURE_READ_MAX:
            nfc_reader.reset()
            self._reset_count = 0
        self._reset_count += 1

        return super().read_card(nfc_reader)
