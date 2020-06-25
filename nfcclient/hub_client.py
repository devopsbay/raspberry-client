import logging
from dataclasses import dataclass
from datetime import datetime

import requests

from nfcclient.settings import settings


class HubClient:
    def __init__(self, hub_host: str):
        self.hub_host = hub_host
        self._session = requests.Session()

    def get_config(self, client_id: str):
        api_call_url = f"{self.hub_host}/config/{client_id}"
        try:
            response = self._session.get(api_call_url)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            logging.critical(f'API Call error: {e}')

    def authenticate_card(self, card_id: str, door_name: str) -> dict:
        api_call_url = f"{self.hub_host}/auth/card/{card_id}/{door_name}"
        try:
            response = self._session.get(api_call_url).json()
            return response

        except requests.exceptions.RequestException as e:
            logging.critical(f'API Call error: {e}')
            return {}


hub_client = HubClient(settings.HUB_HOST_URL)
