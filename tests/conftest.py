import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.db"),
            "RATE_PER_KG": 25.0,
            "MAX_KG_PER_DELIVERY": 150.0,
        }
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def centre(client):
    return client.post("/centres", json={"name": "Kiamokama Buying Centre", "county": "Kisii"}).get_json()


@pytest.fixture
def farmer(client, centre):
    return client.post(
        "/farmers", json={"name": "Mary Wanjiku", "phone": "0712345678", "centre_id": centre["id"]}
    ).get_json()


@pytest.fixture
def record(client, farmer):
    """Helper to record a delivery for the default farmer."""

    def _record(kg, clerk="Otieno", weighed_at="2026-10-05T08:30:00"):
        return client.post(
            "/deliveries",
            json={"farmer_id": farmer["id"], "kg": kg, "clerk": clerk, "weighed_at": weighed_at},
        )

    return _record
