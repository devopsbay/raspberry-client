import asyncio
import logging
from typing import List

from aiohttp import web

from nfcclient.config import ClientConfig
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory, NFCReader

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)

config = ClientConfig.from_env()


async def client_app(client_config: ClientConfig):
    hub_client = client_config.hub_client
    gpio_client = client_config.gpio_client

    readers = []
    logging.info("First Readers Initialise")
    init(client_config, readers)

    logging.info("Start to Listen for cards...")
    try:
        while True:
            await asyncio.sleep(1)
            [asyncio.create_task(
                read_card(client_config, gpio_client, hub_client, reader)
            ) for reader in readers]
    except RuntimeError:
        logging.info("Reinitialise Readers")
        init(client_config, readers)
        logging.info("Start to Listen for cards...")


async def read_card(client_config, gpio_client, hub_client, reader):
    card = reader.read_card()
    if card:
        logging.info('.....CARD Detected.....')
        card_id = "".join([hex(i) for i in card])
        if card_id in client_config.master_keys:
            logging.info(f'Master Card {card_id} Used')
            asyncio.create_task(gpio_client.open_door(reader.door, card_id))
        elif hub_client.is_card_authorized(card_id=card_id, door_id=reader.door):
            asyncio.create_task(gpio_client.open_door(reader.door, card_id))
        else:
            logging.warning(f'Unauthorised Card {card_id}')


def init(client_config: ClientConfig, readers: List[NFCReader]):
    for door in client_config.doors:
        for reader in door.readers:
            try:
                nfc_reader = NFCReaderFactory.create(
                    pin=reader,
                    door=door.name,
                    reader_timeout=client_config.reader_timeout,
                    debug=client_config.debug,
                )
                readers.append(nfc_reader)
                logging.info(f'NFC Reader {reader} for door {door.name} initialised')
            except Exception as e:
                logging.critical(f'NFC Reader {reader} for door {door.name} failed: {e}')


async def aiohttp_server(app, port):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=port)
    await site.start()


if __name__ == "__main__":
    from nfcclient.api import app
    app["config"] = config
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(aiohttp_server(app=app, port=config.web_port))
    event_loop.create_task(client_app(client_config=config))
    event_loop.run_forever()
