import RPi.GPIO as GPIO
from time import sleep
import logging


def gpio_setup(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def gpio_signal(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(5)
    GPIO.output(pin, GPIO.LOW)


def open_door(door, card_id):
    logging.info("Door {} OPEN for {}".format(door, card_id))
    if door == "103":
        gpio_signal(21)
    else:
        gpio_signal(20)
    logging.info("Door {} Closed".format(door))



