import logging

from nfcclient.utils import get_env_var

CLIENT_ID = get_env_var("CLIENT_ID", "1")
HUB_HOST_URL = get_env_var("HUB_HOST_URL", "https://panel.lesnahub.pl")


WEB = {
    "HOST": "localhost",
    "PORT": 8000,
}

DEBUG = False

NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader.NFCReaderImpl"
NFC_REFRESHING_FEATURE = True
NFC_REFRESHING_FEATURE_READ_MAX = 700

READER_TIMEOUT = 0.50
READ_PERIOD = 1

try:
    from .local import *
except ImportError:  # pragma: no cover
    pass

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    )
