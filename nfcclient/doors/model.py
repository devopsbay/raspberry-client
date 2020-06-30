import asyncio
import logging

from nfcclient.gpio_client import gpio_client


class Door:
    name: str
    pin_id: int
    _opened: bool = False
    _closing_task: any

    def __init__(self, name, pin):
        self.name = name
        self.pin_id = pin
        self._closing_task = None
        gpio_client.configure(self.pin_id)

    def is_open(self):
        return self._opened

    async def open(self, seconds: int, remote: bool = False) -> None:
        # 0 seconds has special meaning which is to shutdown the doors
        if seconds == 0:
            self._cancel_closing_doors()
            self._close()
            return

        if self.is_open():
            if remote:
                # if doors are open for remotely opening just cancel scheduled action and set up new
                # otherwise act normally
                self._cancel_closing_doors()
                self._closing_task = asyncio.get_event_loop().call_later(seconds, self._close)
            return

        self._open()

        self._closing_task = asyncio.get_event_loop().call_later(seconds, self._close)

    def _cancel_closing_doors(self):
        if self._closing_task:
            self._closing_task.cancel()
            self._closing_task = None

    def _open(self):
        self._opened = True
        logging.info(f"Door {self.name} OPEN")
        gpio_client.open(pin=self.pin_id)

    def _close(self):
        self._opened = False
        logging.info(f"Door {self.name} Closed")
        gpio_client.close(pin=self.pin_id)

    def clean(self):
        gpio_client.clean(self.pin_id)
