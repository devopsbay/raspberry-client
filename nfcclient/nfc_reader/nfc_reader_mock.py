from nfcclient.nfc_reader.nfc_reader_factory import NFCReader


class NFCReaderMock(NFCReader):
    def __init__(self, pin: str, door: str, reader_timeout: float, debug: bool = False) -> None:
        super().__init__(pin=pin, door=door, reader_timeout=reader_timeout, debug=debug)

    def read_card(self):
        return [43, 21, 39, 12]
