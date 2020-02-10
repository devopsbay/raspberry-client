
'''
2 NFC readers app
'''


import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import requests
import json
import RPi.GPIO as GPIO
from time import *



# Additional import needed for I2C/SPI
from digitalio import DigitalInOut

from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

#first NFC reader
cs_pin_1 = DigitalInOut(board.D24)
pn532_1 = PN532_SPI(spi, cs_pin_1, debug=False)

#first NFC reader
cs_pin_2 = DigitalInOut(board.D23)
pn532_2 = PN532_SPI(spi, cs_pin_2, debug=False)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

#door_identity
enter_door = 101
inside_door = 103

#masters_key
master_keys = ['0x2b0x150x270xc', '0xda0x130x640x1a', '0xca0xbf0x570x1a']

def read_card(reader1, reader2):
    while True:
        # Check if a card is available to read
        uid = pn532_2.read_passive_target(timeout=0.5)
        if uid:
            print('czytnik1: \nFound card with UID:', [hex(i) for i in uid])
            return uid
        uid = pn532_1.read_passive_target(timeout=0.5)
        if uid:
            print('czytnik2: \nFound card with UID:', [hex(i) for i in uid])
            return uid


def open_door():
    print("Door OPEN")
    GPIO.output(21, GPIO.HIGH)
    sleep(5)
    GPIO.output(21, GPIO.LOW)
    print("Door CLOSE")

print("Start waiting for card_id")

ic1, ver1, rev1, support1 = pn532_1.get_firmware_version()
print('Found first PN532 with firmware version: {0}.{1}'.format(ver1, rev1))
pn532_1.SAM_configuration()

ic2, ver2, rev2, support2 = pn532_2.get_firmware_version()
print('Found second PN532 with firmware version: {0}.{1}'.format(ver2, rev2))
pn532_2.SAM_configuration()


# Configure PN532 to communicate with MiFare cards


print('')

while True:
    uid = read_card(pn532_1, pn532_2)
    card_id = ''
    uid = [hex(i) for i in uid]
    for i in uid:
        card_id = card_id + i
    print(card_id)
    if card_id in master_keys:
        open_door()
        continue
    print("http://devopsbay-alb-313417205.eu-west-1.elb.amazonaws.com/auth/card/{}/{}".format(card_id, inside_door))
    r = requests.get("http://devopsbay-alb-313417205.eu-west-1.elb.amazonaws.com/auth/card/{}/{}".format(card_id, inside_door))
    r = r.json()
    if r['status'] == True:
        open_door()
    else:
        print("DRZWI ZAMKNIETE")

GPIO.cleanup()

