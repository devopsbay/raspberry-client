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


def client_app():
    client_config = ClientConfig.from_env()

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, GPIO.LOW)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW)

    readers = []
    logging.info("First Readers Initialise")
    for door in client_config.doors:
        for reader in door['readers']:
            try:
                nfc_reader = NFCReader(client_config, pin=reader, door=door['name'])
                readers.append(nfc_reader)
                logging.info('NFC Reader {} for door {} initialised'.format(reader, door['name']))
            except Exception as e:
                logging.critical('NFC Reader {} for door {} failed: {}'.format(reader, door['name'], e))

    logging.info("Start to Listen for cards...")
    while True:
        try:
            for reader in readers:
                sleep(1)
                card = reader.read_card()
                if card:
                    logging.info('.....CARD Detected.....')
                    card_id = "".join(reader.hex_uid(card))
                    if card_id in client_config.master_keys:
                        logging.info('Master Card {} Used'.format(card_id))
                        api_call_url = "{}/auth/card/{}/{}".format(client_config.hub_host, card_id, door)
                        open_door(reader.door, card_id)
                        continue
                    elif auth_api_call(client_config, card_id, reader.door):
                        open_door(reader.door, card_id)
                        continue
                    else:
                        logging.warning('Unauthorised Card {}'.format(card_id))
        except RuntimeError:
            logging.info("Reinitialise Readers")
            for door in client_config.doors:
                for reader in door['readers']:
                    try:
                        nfc_reader = NFCReader(client_config, pin=reader, door=door['name'])
                        readers.append(nfc_reader)
                        logging.info('NFC Reader {} for door {} initialised'.format(reader, door['name']))
                    except Exception as e:
                        logging.critical('NFC Reader {} for door {} failed: {}'.format(reader, door['name'], e))

            logging.info("Start to Listen for cards...")
            continue


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
