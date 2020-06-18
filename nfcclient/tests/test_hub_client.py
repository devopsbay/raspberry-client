import pytest
import requests

from nfcclient.hub_client import HubClient


@pytest.fixture
def hub_client():
    return HubClient("http://localhost:8000")


def test_is_card_authorized(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/2", json={"status": True})
    assert hub_client.is_card_authorized(card_id="1", door_id="2")


def test_is_card_authorized_false(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/3", json={"status": False})
    assert hub_client.is_card_authorized(card_id="1", door_id="3") is False


def test_is_card_authorized_not_found(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/4", exc=requests.exceptions.ConnectTimeout)
    assert hub_client.is_card_authorized(card_id="1", door_id="4") is False
