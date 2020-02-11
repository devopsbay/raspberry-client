from time import sleep
import requests

from .config import ClientConfig
from .nfc_reader import NFCReader

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('No GPIO library found')
    GPIO = None

'''
NFC readers app
'''


def client_app():
    client_config = ClientConfig.from_env()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, GPIO.LOW)

    readers = []
    print("Start waiting for card_id")
    for door in client_config.doors:
        for reader in door['readers']:
            nfc_reader = NFCReader(client_config, pin=reader, door=door)
            readers.append(nfc_reader)

    while True:
        for reader in readers:
            uid = reader.read_card()
            card_id = ''
            for i in uid:
                card_id = card_id + i
            print(card_id)

            if card_id in client_config.master_keys:
                open_door()
                continue
            print("{}/auth/card/{}/{}".format(client_config.hub_host, card_id, reader.door))
            r = requests.get(
                "http://devopsbay-alb-313417205.eu-west-1.elb.amazonaws.com/auth/card/{}/{}".format(card_id,
                                                                                                    reader.door))
            r = r.json()
            if r['status'] == True:
                open_door()
            else:
                print("DRZWI ZAMKNIETE")

    GPIO.cleanup()


def open_door():
    print("Door OPEN")
    GPIO.output(21, GPIO.HIGH)
    sleep(5)
    GPIO.output(21, GPIO.LOW)
    print("Door CLOSE")


if __name__ == "__main__":
    client_app()
