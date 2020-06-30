import pytest

from nfcclient.utils import get_env_var, ConfigError


def test_get_env_var(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "1")
    assert get_env_var("CLIENT_ID") == "1"


def test_get_env_var_with_prefix(monkeypatch):
    monkeypatch.setenv("PRF_CLIENT_ID", "1")
    assert get_env_var("CLIENT_ID", prefix="PRF") == "1"


def test_get_env_var_allow_empty(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    assert get_env_var("CLIENT_ID", allow_empty=True) is None


def test_get_env_var_default(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    assert get_env_var("CLIENT_ID", default="120") is "120"


def test_get_env_var_except(monkeypatch):
    monkeypatch.delenv("CLIENT_ID", raising=False)
    with pytest.raises(ConfigError):
        get_env_var("CLIENT_ID")
