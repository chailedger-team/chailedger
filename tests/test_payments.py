from app.payments.service import calculate_payout


def test_calculate_payout():
    assert calculate_payout(100, 25) == 2500
    assert calculate_payout(12.345, 25) == 308.62
    assert calculate_payout(0, 25) == 0


def test_statement_only_pays_confirmed_kg(client, farmer, record):
    confirmed = record(20, weighed_at="2026-10-01T08:00:00").get_json()
    disputed = record(15, weighed_at="2026-10-02T08:00:00").get_json()
    record(10, weighed_at="2026-10-03T08:00:00")  # stays pending
    record(50, weighed_at="2026-09-30T08:00:00")  # different month

    client.post(f"/deliveries/{confirmed['id']}/confirm")
    client.post(f"/deliveries/{disputed['id']}/dispute", json={"farmer_kg": 16, "reason": "low"})

    res = client.get(f"/farmers/{farmer['id']}/statement?month=2026-10")
    assert res.status_code == 200
    s = res.get_json()
    assert s["farmer_no"] == "CL-0001"
    assert len(s["deliveries"]) == 3
    assert s["kg_confirmed"] == 20
    assert s["kg_disputed"] == 15
    assert s["kg_pending"] == 10
    assert s["estimated_payout"] == 500
    assert s["currency"] == "KES"


def test_statement_for_empty_month(client, farmer):
    s = client.get(f"/farmers/{farmer['id']}/statement?month=2026-01").get_json()
    assert s["deliveries"] == []
    assert s["estimated_payout"] == 0


def test_statement_errors(client, farmer):
    assert client.get("/farmers/999/statement").status_code == 404
    assert client.get(f"/farmers/{farmer['id']}/statement?month=Oct").status_code == 400
