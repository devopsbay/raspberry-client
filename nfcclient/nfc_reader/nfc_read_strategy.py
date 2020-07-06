import asyncio
import logging

from nfcclient.settings import settings


class ReadStrategy:
    def read_card(self, nfc_reader):
        raise NotImplementedError


class BasicReadStrategy(ReadStrategy):
    def read_card(self, nfc_reader):
        uid = nfc_reader.pn532.read_passive_target(timeout=nfc_reader.reader_timeout)
        if uid:
            logging.info(
                f'Door {nfc_reader.door}:{nfc_reader.pin._pin} : Found card with UID: {"".join([hex(i) for i in uid])}'
            )
            return uid


class RefreshingReadStrategy(ReadStrategy):
    _reset_count: int = 0

    def __init__(self, basic_read_strategy):
        self.basic_read_strategy = basic_read_strategy

    def read_card(self, nfc_reader):
        if self._reset_count == settings.NFC_REFRESHING_FEATURE_READ_MAX:
            asyncio.get_event_loop().create_task(nfc_reader.reset())
            self._reset_count = 0
            return

        self._reset_count += 1
        return self.basic_read_strategy.read_card(nfc_reader)
