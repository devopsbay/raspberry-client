import logging

import aiohttp
from aiohttp import web


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app["websockets"].append(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == "close":
                await ws.close()
            else:
                for _ws in request.app["websockets"]:
                    await _ws.send_str(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logging.debug(f"ws connection closed with exception {ws.exception()}")

    request.app["websockets"].remove(ws)

    return ws