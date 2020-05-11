import logging
from time import sleep
import requests

from config import ClientConfig
from nfc_reader import NFCReader

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

try:
    import RPi.GPIO as GPIO
except ImportError:
    print('No GPIO library found')
    GPIO = None

'''
NFC readers app
'''


def init_readers(client_config):
    readers = []
    logging.info("Initialise Readers")
    for door in client_config.doors:
        for reader in door['readers']:
            try:
                nfc_reader = NFCReader(client_config, pin=reader, door=door['name'])
                readers.append(nfc_reader)
                logging.info('NFC Reader {} for door {} initialised'.format(reader, door['name']))
            except Exception as e:
                logging.critical('NFC Reader {} for door {} failed: {}'.format(reader, door['name'], e))
                continue
    return readers


def read_from_card(reader, client_config):
    try:
        card = reader.read_card()
        if card:
            logging.info('.....CARD Detected.....')
            card_id = "".join(reader.hex_uid(card))
            if card_id in client_config.master_keys:
                logging.info('Master Card {} Used'.format(card_id))
                open_door(reader.door, card_id)
            elif auth_api_call(client_config, card_id, reader.door):
                open_door(reader.door, card_id)
            else:
                logging.warning('Unauthorised Card {}'.format(card_id))
    except Exception as e:
        logging.critical('NFC Reader {} failed: {}'.format(reader, e))


def client_app():
    client_config = ClientConfig.from_env()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, GPIO.LOW)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW)

    readers = init_readers(client_config)
    loop_counter = 0
    logging.info("Start to Listen for cards...")

    while True:
        for reader in readers:
            read_from_card(reader, client_config)
        loop_counter += 1
        if loop_counter % 20:
            logging.info('Re-init Readers')
            readers = init_readers(client_config)


def auth_api_call(client_config, card_id, door):
    api_call_url = "{}/auth/card/{}/{}".format(client_config.hub_host, card_id, door)
    logging.debug(api_call_url)
    try:
        api_request = requests.get(api_call_url).json()
        if api_request.get('status') == True:
            logging.info('API Call ')
            return True
    except requests.exceptions.RequestException as e:
        logging.critical('API Call error: {}'.format(e))
    return False


def open_door(door, card_id):
    logging.info("Door {} OPEN for {}".format(door, card_id))
    if door == "103":
        GPIO.output(21, GPIO.HIGH)
        sleep(5)
        GPIO.output(21, GPIO.LOW)
    else:
        GPIO.output(20, GPIO.HIGH)
        sleep(5)
        GPIO.output(20, GPIO.LOW)
    logging.info("Door {} Closed".format(door))


if __name__ == "__main__":
    client_app()
