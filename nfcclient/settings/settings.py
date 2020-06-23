import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)

WEB = {
    "HOST": "localhost",
    "PORT": 8000,
}

DEBUG = False

HUB_HOST = "https://dev.panel.lesnahub.pl"

NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader.NFCReaderImpl"

READER_TIMEOUT = 0.5

try:
    from .local import *
except ImportError:
    pass
