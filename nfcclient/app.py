import logging
import os
from datetime import datetime
from time import sleep
import requests

from config import ClientConfig
from nfc_reader import NFCReader

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('No GPIO library found')
    GPIO = None

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

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
    print("Initialise Readers")
    for door in client_config.doors:
        for reader in door['readers']:
            try:
                nfc_reader = NFCReader(client_config, pin=reader, door=door['name'])
                readers.append(nfc_reader)
                logging.info('NFC Reader {} for door {} initialised'.format(reader, door['name']))
            except Exception as e:
                logging.error('NFC Reader {} for door {} failed: {}'.format(reader, door['name'], e))

    logging.info("Start to Listen for cards...")
    while True:
        for reader in readers:
            card_id = reader.read_card()
            if card_id:
                if str(card_id) in client_config.master_keys:
                    logging.info('Master Card {} Used'.format(card_id))
                    open_door(reader.door, card_id)
                    continue
                elif auth_api_call(client_config, str(card_id), reader.door):
                    open_door(reader.door, card_id)
                    continue
                else:
                    logging.warning('Unauthorised Card {} - {}'.format(card_id, datetime.now()))


def auth_api_call(client_config, card_id, door):
    api_call_url = "{}/auth/card/{}/{}".format(client_config.hub_host, card_id, door)
    logging.debug(api_call_url)
    try:
        api_request = requests.get(api_call_url).json()
        if api_request.get('status') == True:
            logging.info('API Call ')
            return True
    except requests.exceptions.RequestException as e:
        logging.error('API Call error: {}'.format(e))
    return False


def open_door(door, card_id):
    logging.info("{} - Door {} OPEN for {}".format( datetime.now(), door, card_id))
    GPIO.output(21, GPIO.HIGH)
    sleep(5)
    GPIO.output(21, GPIO.LOW)
    logging.info("Door {} Closed".format(door))


if __name__ == "__main__":
    client_app()
