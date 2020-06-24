import asyncio
import logging

from nfcclient.gpio_client import gpio_client
from nfcclient.hub_client import hub_client, AuthUser
from nfcclient.nfc_reader.nfc_reader_factory import NFCReader


async def read_card(config, reader: NFCReader):
    card = reader.read_card()
    if card:
        logging.info('.....CARD Detected.....')
        card_id = "".join([hex(i) for i in card])
        door_name = reader.door
        user = hub_client.authenticate_card(card_id=card_id, door_name=door_name)
        if await authorize(config=config, user=user, card_id=card_id):
            asyncio.create_task(gpio_client.open_door(reader.door))


async def authorize(config, user: AuthUser, card_id: str) -> bool:
    if card_id in config.master_keys:
        logging.info(f'Master Card {card_id} Used')
        return True

    if user.is_authorized():
        logging.info(f"{card_id} Used")
        return True

    logging.warning(f'Unauthorized Card {card_id}')
    return False
