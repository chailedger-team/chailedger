import importlib

import pytest

import app.config as config_module
from app import create_app


@pytest.fixture(autouse=True)
def restore_config():
    yield
    importlib.reload(config_module)


def reload_config(monkeypatch, **env):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config_module).Config


def test_database_path_comes_from_environment(monkeypatch):
    config = reload_config(monkeypatch, CHAILEDGER_DATABASE="/app/data/chailedger.db")
    assert config.DATABASE == "/app/data/chailedger.db"


def test_rate_and_max_kg_are_numbers(monkeypatch):
    config = reload_config(monkeypatch, CHAILEDGER_RATE_PER_KG="30", CHAILEDGER_MAX_KG_PER_DELIVERY="120")
    assert config.RATE_PER_KG == 30.0
    assert config.MAX_KG_PER_DELIVERY == 120.0


def test_app_creates_database_in_new_folder(tmp_path):
    db_path = tmp_path / "data" / "chailedger.db"
    app = create_app({"TESTING": True, "DATABASE": str(db_path)})
    assert db_path.exists()
    assert app.test_client().get("/health").get_json() == {"status": "ok"}
