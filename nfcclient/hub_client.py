import logging

import aiohttp

from nfcclient.settings import settings


class HubClient:
    def __init__(self, hub_host: str):
        self.hub_host = hub_host

    async def get_config(self, client_id: str):
        api_call_url = f"{self.hub_host}/config/{client_id}"
        return await self._request(url=api_call_url)

    async def authenticate_card(self, card_id: str, door_name: str) -> dict:
        api_call_url = f"{self.hub_host}/auth/card/{card_id}/{door_name}"
        return await self._request(url=api_call_url)

    async def _request(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        except Exception as e:
            logging.critical(f'API Call error: {e}')
            return {}


hub_client = HubClient(settings.HUB_HOST_URL)
