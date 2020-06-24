import asyncio

import aiohttp_jinja2
from aiohttp import web

from nfcclient.gpio_client import gpio_client


async def refresh(request):
    request.app["config"].refresh_from_server()
    return web.json_response({"status": "ok"})


async def open_door(request):
    door_name = request.match_info["door_name"]
    seconds = int(request.rel_url.query.getone("seconds", gpio_client.door_open_seconds))
    asyncio.create_task(gpio_client.open_door(door_name=door_name, seconds=seconds))
    return web.json_response({"status": "ok"})


@aiohttp_jinja2.template("index.jinja2")
async def index(request):
    return {}
