import pytest
from aioresponses import aioresponses

from nfcclient.hub_client import HubClient

pytestmark = pytest.mark.asyncio


@pytest.fixture
def hub_client():
    return HubClient("http://localhost:8000")


async def test_is_card_authorized(hub_client):
    with aioresponses() as mocked:
        mocked.get("http://localhost:8000/auth/card/1/2", payload={"status": True})
        auth = await hub_client.authenticate_card(card_id="1", door_name="2")
        assert auth == {"status": True}


async def test_is_card_authorized_false(hub_client):
    with aioresponses() as mocked:
        mocked.get("http://localhost:8000/auth/card/1/3", payload={"status": False})
        auth = await hub_client.authenticate_card(card_id="1", door_name="3")
        assert auth == {"status": False}


async def test_authenticate_card_request_failed(hub_client, caplog):
    with aioresponses() as mocked:
        mocked.get("http://localhost:8000/auth/card/1/4", exception=Exception("LOL"))
        auth = await hub_client.authenticate_card(card_id="1", door_name="4")
        assert "API Call error" in caplog.text
        assert auth == {}


async def test_get_config_failed(hub_client, caplog):
    with aioresponses() as mocked:
        mocked.get("http://localhost:8000/config/1", exception=Exception("LOL"))
        response = await hub_client.get_config(client_id="1")
        assert "API Call error" in caplog.text
        assert response == {}
