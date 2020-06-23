import asyncio
import logging
from typing import List

from nfcclient.card_reader import read_card
from nfcclient.config import ClientConfig
from nfcclient.http_server import aiohttp_server, app
from nfcclient.nfc_reader.nfc_reader_factory import NFCReaderFactory, NFCReader
from nfcclient.settings import settings

config = ClientConfig.from_env()


async def client_app(client_config: ClientConfig):
    readers = []
    logging.info("First Readers Initialise")
    await init(client_config, readers)
    try:
        while True:
            await asyncio.sleep(1)
            [asyncio.create_task(
                read_card(client_config, reader)
            ) for reader in readers]
    except RuntimeError:
        logging.info("Reinitialise Readers")
        await init(client_config, readers)


async def init(client_config: ClientConfig, readers: List[NFCReader]):
    for door in client_config.doors:
        for reader in door.readers:
            try:
                nfc_reader = NFCReaderFactory.create(
                    pin=reader,
                    door=door.name,
                    reader_timeout=settings.READER_TIMEOUT,
                    debug=settings.DEBUG,
                )
                readers.append(nfc_reader)
                logging.info(f'NFC Reader {reader} for door {door.name} initialised')
            except Exception as e:
                logging.critical(f'NFC Reader {reader} for door {door.name} failed: {e}')

    logging.info("Start to Listen for cards...")


if __name__ == "__main__":
    app["config"] = config
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(aiohttp_server(app=app, host=settings.WEB["HOST"], port=settings.WEB["PORT"]))
    event_loop.create_task(client_app(client_config=config))
    event_loop.run_forever()
