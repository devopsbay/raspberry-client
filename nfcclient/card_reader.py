import asyncio
import logging

from nfcclient.nfc_reader.nfc_reader_factory import NFCReader


async def read_card(config, reader: NFCReader):
    card = reader.read_card()
    if card:
        logging.info('.....CARD Detected.....')
        card_id = "".join([hex(i) for i in card])
        door_name = reader.door
        if await authorize(config=config, card_id=card_id, door_name=door_name):
            asyncio.create_task(config.gpio_client.open_door(reader.door))


async def authorize(config, card_id: str, door_name: str) -> bool:
    if card_id in config.master_keys:
        config.hub_client.authenticate_card(card_id=card_id, door_name=door_name)
        logging.info(f'Master Card {card_id} Used')
        return True

    if config.hub_client.is_card_authorized(card_id=card_id, door_name=door_name):
        logging.info(f"{card_id} Used")
        return True

    logging.warning(f'Unauthorized Card {card_id}')
    return False
