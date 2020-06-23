import aiohttp_jinja2
import jinja2
from aiohttp import web

from nfcclient.router import routes
from nfcclient.settings import settings


async def aiohttp_server(app, host: str, port: int):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()


app = web.Application()
app["websockets"] = []
app["websocket_url"] = settings.WEBSOCKET_URL
app.router.add_static(prefix=settings.STATIC_URL, path=settings.STATIC_DIR, name='static')
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader("templates")
)
