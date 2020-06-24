from fake_rpi.RPi import GPIO

from nfcclient.gpio_client import GPIOClient


def test_gpio_init(mocker):
    mocker.patch("fake_rpi.RPi.GPIO.setmode")
    GPIOClient()
    GPIO.setmode.assert_called_once_with(GPIO.BCM)


def test_gpio_configure(mocker):
    mocker.patch("fake_rpi.RPi.GPIO.setup")
    mocker.patch("fake_rpi.RPi.GPIO.output")
    GPIOClient().configure(21)
    GPIO.setup.assert_called_once_with(21, GPIO.OUT)
    GPIO.output.assert_called_once_with(21, GPIO.LOW)


def test_gpio_open(mocker):
    mocker.patch("fake_rpi.RPi.GPIO.output")
    GPIOClient().open(21)
    GPIO.output.assert_called_once_with(21, GPIO.HIGH)


def test_gpio_close(mocker):
    mocker.patch("fake_rpi.RPi.GPIO.output")
    GPIOClient().close(21)
    GPIO.output.assert_called_once_with(21, GPIO.LOW)

