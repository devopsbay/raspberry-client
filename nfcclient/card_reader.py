import asyncio
import logging

from nfcclient.config import ClientConfig
from nfcclient.doors.manager import door_manager
from nfcclient.hub_client import hub_client
from nfcclient.nfc_reader.nfc_reader import NFCReader
from nfcclient.nfc_reader.nfc_reader_manager import nfc_reader_manager
from nfcclient.settings import settings


async def runner(client_config: ClientConfig) -> None:
    while True:
        await read_cards(client_config=client_config)


async def read_cards(client_config: ClientConfig) -> None:
    try:
        await asyncio.sleep(settings.READ_PERIOD)
        for door in door_manager.all_by_not_opened():
            for reader in nfc_reader_manager.all_by_door_name(door_name=door.name):
                await read_card(client_config, reader)
    except RuntimeError as e:
        logging.critical(f"Critical error: {e}")
        logging.info("Reinitialise Readers")
        nfc_reader_manager.configure(doors=client_config.doors)


async def read_card(config, reader: NFCReader) -> None:
    logging.debug(f"Read card for doors {reader.door}:{reader.pin_number}")
    card = reader.read_card()
    if card:
        card_id = "".join([hex(i) for i in card])
        door_name = reader.door
        auth = await hub_client.authenticate_card(card_id=card_id, door_name=door_name)
        if await authorize(config=config, auth=auth, card_id=card_id):
            asyncio.get_event_loop().create_task(door_manager.get(reader.door).open(config.door_open_seconds))


async def authorize(config, auth: dict, card_id: str) -> bool:
    if card_id in config.master_keys:
        logging.info(f'Master Card {card_id} Used')
        return True

    if auth.get("status", False):
        logging.info(f"{card_id} Used")
        return True

    logging.warning(f'Unauthorized Card {card_id}')
    return False
