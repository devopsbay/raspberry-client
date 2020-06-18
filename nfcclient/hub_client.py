import logging

import requests
from rest_framework.status import HTTP_200_OK


class HubClient:
    def __init__(self, hub_host: str):
        self.hub_host = hub_host
        self._session = requests.Session()

    def get_config(self, client_id: str):
        api_call_url = f"{self.hub_host}/config/{client_id}"
        try:
            response = self._session.get(api_call_url)
            if response.status_code == HTTP_200_OK:
                return response.json()
        except requests.exceptions.RequestException as e:
            logging.critical(f'API Call error: {e}')

    def is_card_authorized(self, card_id: str, door_id: str) -> bool:
        api_call_url = f"{self.hub_host}/auth/card/{card_id}/{door_id}"
        logging.debug(api_call_url)
        try:
            response = self._session.get(api_call_url).json()
            if response.get('status'):
                logging.info('API Call')
                return True
        except requests.exceptions.RequestException as e:
            logging.critical(f'API Call error: {e}')
        return False
