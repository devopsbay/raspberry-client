import asyncio

from aiohttp import web

from nfcclient.doors.manager import door_manager

async def health_check(request):
    return web.json_response({"status": "ok"})

async def restart_readers(request):
    asyncio.get_event_loop().create_task(request.app["config"].refresh_from_envs())
    return web.json_response({"status": "ok"})

async def refresh(request):
    asyncio.get_event_loop().create_task(request.app["config"].refresh_from_server())
    return web.json_response({"status": "ok"})


async def open_door(request):
    door_name = request.match_info["door_name"]
    seconds = int(request.rel_url.query.getone("seconds", request.app["config"].door_open_seconds))
    asyncio.get_event_loop().create_task(door_manager.get(name=door_name).open(seconds=seconds, remote=True))
    return web.json_response({"status": "ok"})
