import asyncio
import logging

from nfcclient.config import ClientConfig
from nfcclient.doors.manager import door_manager
from nfcclient.hub_client import hub_client
from nfcclient.nfc_reader.nfc_reader import NFCReader
from nfcclient.nfc_reader.nfc_reader_manager import nfc_reader_manager
from nfcclient.settings import settings


async def runner(client_config: ClientConfig) -> None:
    reader = CardReaderFacade(client_config=client_config)
    while True:
        await reader.read_cards()


class CardReaderFacade:
    def __init__(self, client_config: ClientConfig):
        self.config = client_config
        self.event_loop = asyncio.get_event_loop()
        self.tasks = {}

    async def read_cards(self) -> None:
        try:
            await asyncio.sleep(settings.READ_PERIOD)
            for door in door_manager.all_by_not_opened():
                for reader in nfc_reader_manager.all_idle_by_door_name(door_name=door.name):
                    pin = reader.pin_number
                    if pin not in self.tasks:
                        task = self.event_loop.create_task(self.read_card(reader))
                        task.add_done_callback(self._pop_finished_task)
                        self.tasks[pin] = task
        except RuntimeError as e:
            logging.critical(f"Critical error: {e}")
            logging.info("Reinitialise Readers")
            nfc_reader_manager.configure(doors=self.config.doors)

    async def read_card(self, reader: NFCReader) -> None:
        logging.debug(f"Read card for doors {reader.door}:{reader.pin_number}")
        card = reader.read_card()
        if card:
            card_id = "".join([hex(i) for i in card])
            door_name = reader.door
            auth = await hub_client.authenticate_card(card_id=card_id, door_name=door_name)
            if await self.authorize(auth=auth, card_id=card_id):
                self.event_loop.create_task(door_manager.get(reader.door).open(self.config.door_open_seconds))

    async def authorize(self, auth: dict, card_id: str) -> bool:
        if card_id in self.config.master_keys:
            logging.info(f'Master Card {card_id} Used')
            return True

        if auth.get("status", False):
            logging.info(f"{card_id} Used")
            return True

        logging.warning(f'Unauthorized Card {card_id}')
        return False

    def _pop_finished_task(self, task):
        for key, value in list(self.tasks.items()):
            if value == task:
                self.tasks.pop(key)
