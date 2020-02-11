from time import sleep
import requests

from config import ClientConfig, logger
from nfc_reader import NFCReader

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
    logger.info("Initialise Readers")
    for door in client_config.doors:
        for reader in door['readers']:
            try:
                nfc_reader = NFCReader(client_config, pin=reader, door=door['name'])
                readers.append(nfc_reader)
                logger.info('NFC Reader {} for door {} initialised'.format(reader, door['name']))
            except Exception as e:
                logger.critical('NFC Reader {} for door {} failed: {}'.format(reader, door['name'], e))

    logger.info("Start to Listen for cards...")
    while True:
        for reader in readers:
            card = reader.read_card()
            if card:
                card_id = "".join(reader.hex_uid(card))
                if card_id in client_config.master_keys:
                    logger.info('Master Card {} Used'.format(card_id))
                    open_door(reader.door, card_id)
                    continue
                elif auth_api_call(client_config, card_id, reader.door):
                    open_door(reader.door, card_id)
                    continue
                else:
                    logger.warning('Unauthorised Card {}'.format(card_id))


def auth_api_call(client_config, card_id, door):
    api_call_url = "{}/auth/card/{}/{}".format(client_config.hub_host, card_id, door)
    logger.debug(api_call_url)
    try:
        api_request = requests.get(api_call_url).json()
        if api_request.get('status') == True:
            logger.info('API Call ')
            return True
    except requests.exceptions.RequestException as e:
        logger.critical('API Call error: {}'.format(e))
    return False


def open_door(door, card_id):
    logger.info("Door {} OPEN for {}".format(door, card_id))
    GPIO.output(21, GPIO.HIGH)
    sleep(5)
    GPIO.output(21, GPIO.LOW)
    logger.info("Door {} Closed".format(door))


if __name__ == "__main__":
    client_app()
