import os
import sys

import fake_rpi

WEB = {
    "HOST": "localhost",
    "PORT": 8000,
}

DEBUG = True

HUB_URL = "http://localhost"
WEBSOCKET_URL = f"ws://{WEB['HOST']}:{WEB['PORT']}/ws"

NFC_READER_MODULE = "nfcclient.nfc_reader.nfc_reader_mock.NFCReaderMock"

os.environ["BLINKA_FORCEBOARD"] = 'RASPBERRY_PI_4B'
os.environ["BLINKA_FORCECHIP"] = 'BCM2XXX'
sys.modules["RPi"] = fake_rpi.RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
