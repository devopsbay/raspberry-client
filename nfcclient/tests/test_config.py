import pytest

from nfcclient.config import get_env_var, ConfigError, Door


def test_get_env_var(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1")
    assert get_env_var("CLIENT_ID") == "1"


def test_get_env_var_with_prefix(monkeypatch):
    monkeypatch.setenv("PRF_CLIENT_ID", "1")
    assert get_env_var("CLIENT_ID", prefix="PRF") == "1"


def test_get_env_var_allow_empty(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    assert get_env_var("CLIENT_ID", allow_empty=True) is None


def test_get_env_var_except(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    with pytest.raises(ConfigError):
        get_env_var("CLIENT_ID")


def test_client_config_from_env(config):
    assert config.client_id == "1123"
    assert config.master_keys == ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]
    assert config.doors == [Door(name="103", pin_id=21, readers=["D23", "D24"])]
    assert config.reader_timeout == 0.5
    assert config.gpio_client.door_open_seconds == 1


def test_client_config_refresh_from_server(monkeypatch, requests_mock, config):
    requests_mock.get("http://localhost:8123/config/1123", json={
        "master_keys": ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"],
        "doors": [{"name": "111", "pin_id": 22, "readers": ["D23", "D24"]}],
        "reader_timeout": 0.5,
        "door_open_seconds": 2,
    })

    config.refresh_from_server()

    assert config.client_id == "1123"
    assert config.master_keys == ["0x2b0x150x270xc", "0xda0x130x640x1a", "0xca0xbf0x570x1a", "0xa0x720xa90x15"]
    assert config.doors == [Door(name="111", pin_id=22, readers=["D23", "D24"])]
    assert config.reader_timeout == 0.5
    assert config.gpio_client.door_open_seconds == 2
