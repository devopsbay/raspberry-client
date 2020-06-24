import asyncio

from aiohttp import web

from nfcclient.doors.manager import door_manager


async def refresh(request):
    request.app["config"].refresh_from_server()
    return web.json_response({"status": "ok"})


async def open_door(request):
    door_name = request.match_info["door_name"]
    seconds = int(request.rel_url.query.getone("seconds", request.app["config"].door_open_seconds))
    asyncio.create_task(door_manager.get(name=door_name).open(seconds=seconds, remote=True))
    return web.json_response({"status": "ok"})
