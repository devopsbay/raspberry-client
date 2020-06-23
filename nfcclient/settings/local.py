import os
import sys

import fake_rpi

WEB = {
    "HOST": "localhost",
    "PORT": 8000,
}

DEBUG = True

HUB_HOST_URL = "http://localhost"

NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock"

os.environ["BLINKA_FORCEBOARD"] = 'RASPBERRY_PI_4B'
os.environ["BLINKA_FORCECHIP"] = 'BCM2XXX'
sys.modules["RPi"] = fake_rpi.RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
