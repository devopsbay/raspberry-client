import asyncio
import logging

from nfcclient.card_reader import read_card
from nfcclient.config import ClientConfig
from nfcclient.http_server import aiohttp_server, app
from nfcclient.nfc_reader.nfc_reader_manager import nfc_reader_manager
from nfcclient.settings import settings


async def client_app(client_config: ClientConfig):
    loop = asyncio.get_event_loop()
    while True:
        try:
            await asyncio.sleep(0.5)
            [loop.create_task(
                read_card(client_config, reader)
            ) for reader in nfc_reader_manager.all()]
        except RuntimeError as e:
            logging.critical(f"Critical error: {e}")
            logging.info("Reinitialise Readers")
            nfc_reader_manager.configure(doors=config.doors)


if __name__ == "__main__":
    config = ClientConfig.from_env()
    try:
        app["config"] = config
        event_loop = asyncio.get_event_loop()
        event_loop.create_task(aiohttp_server(app=app, host=settings.WEB["HOST"], port=settings.WEB["PORT"]))
        event_loop.create_task(client_app(client_config=config))
        event_loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Application shutdown")
    finally:
        config.clean()
