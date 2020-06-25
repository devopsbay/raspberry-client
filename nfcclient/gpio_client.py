try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO


class GPIOClient:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def configure(self, pin: int) -> None:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def open(self, pin: int) -> None:
        GPIO.output(pin, GPIO.HIGH)

    def close(self, pin: int) -> None:
        GPIO.output(pin, GPIO.LOW)


gpio_client = GPIOClient()
