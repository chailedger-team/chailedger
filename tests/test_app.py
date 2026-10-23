def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_index_lists_endpoints(client):
    body = client.get("/").get_json()
    assert body["service"] == "ChaiLedger"
    assert any("/deliveries" in e for e in body["endpoints"])


def test_unknown_route_returns_json_404(client):
    res = client.get("/does-not-exist")
    assert res.status_code == 404
    assert "error" in res.get_json()
