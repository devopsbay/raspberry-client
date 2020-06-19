import pytest
import requests

from nfcclient.hub_client import HubClient


@pytest.fixture
def hub_client():
    return HubClient("http://localhost:8000")


def test_is_card_authorized(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/2", json={"status": True})
    assert hub_client.is_card_authorized(card_id="1", door_name="2") is True


def test_is_card_authorized_false(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/3", json={"status": False})
    assert hub_client.is_card_authorized(card_id="1", door_name="3") is False


def test_is_card_authorized_not_found(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/4", exc=requests.exceptions.ConnectTimeout)
    assert hub_client.is_card_authorized(card_id="1", door_name="4") is False


def test_authenticate_card(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/4", json={"status": True})
    response = hub_client.authenticate_card(card_id="1", door_name="4")
    assert response.status_code == 200
    assert response.json() == {"status": True}


def test_authenticate_failed(hub_client, requests_mock):
    requests_mock.get("http://localhost:8000/auth/card/1/4", json={"status": False})
    response = hub_client.authenticate_card(card_id="1", door_name="4")
    assert response.status_code == 200
    assert response.json() == {"status": False}


def test_authenticate_card_request_failed(hub_client, requests_mock, caplog):
    requests_mock.get("http://localhost:8000/auth/card/1/4", exc=requests.exceptions.ConnectTimeout)
    response = hub_client.authenticate_card(card_id="1", door_name="4")
    assert "API Call error" in caplog.text
    assert response is None


def test_get_config_failed(hub_client, requests_mock, caplog):
    requests_mock.get("http://localhost:8000/config/1", exc=requests.exceptions.ConnectTimeout)
    response = hub_client.get_config(client_id="1")
    assert "API Call error" in caplog.text
    assert response is None
