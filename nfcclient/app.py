import asyncio
import logging

from nfcclient.card_reader import runner
from nfcclient.config import ClientConfig
from nfcclient.http_server import aiohttp_server, app
from nfcclient.settings import settings

if __name__ == "__main__":
    config = ClientConfig.from_env()
    try:
        app["config"] = config
        event_loop = asyncio.get_event_loop()
        event_loop.create_task(aiohttp_server(app=app, host=settings.WEB["HOST"], port=settings.WEB["PORT"]))
        event_loop.create_task(runner(client_config=config))
        event_loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Application shutdown")
    finally:
        config.clean()
