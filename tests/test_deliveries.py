def test_record_delivery_starts_pending_and_sends_sms(client, farmer, record):
    res = record(12.5)
    assert res.status_code == 201
    delivery = res.get_json()
    assert delivery["status"] == "pending"
    assert delivery["kg"] == 12.5
    assert delivery["centre_id"] == farmer["centre_id"]

    outbox = client.get("/notifications/outbox?phone=0712345678").get_json()
    assert len(outbox) == 1
    assert "12.5 kg" in outbox[0]["message"]
    assert f"Ref #{delivery['id']}" in outbox[0]["message"]


def test_record_delivery_validation(client, farmer, record):
    assert record(0).status_code == 400
    assert record(500).status_code == 400
    assert client.post("/deliveries", json={"farmer_id": farmer["id"], "kg": 10}).status_code == 400
    assert client.post("/deliveries", json={"farmer_id": 99, "kg": 10, "clerk": "X"}).status_code == 404


def test_confirm_delivery(client, record):
    delivery = record(10).get_json()
    res = client.post(f"/deliveries/{delivery['id']}/confirm")
    assert res.status_code == 200
    assert res.get_json()["status"] == "confirmed"
    assert res.get_json()["resolved_at"] is not None


def test_dispute_delivery_records_farmer_weight(client, record):
    delivery = record(10).get_json()
    res = client.post(
        f"/deliveries/{delivery['id']}/dispute",
        json={"farmer_kg": 11, "reason": "Scale read low; my sack weighed 11 kg at home"},
    )
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "disputed"
    assert body["farmer_kg"] == 11
    # Receipt SMS plus dispute acknowledgement SMS
    assert len(client.get("/notifications/outbox").get_json()) == 2


def test_resolved_delivery_cannot_change(client, record):
    delivery = record(10).get_json()
    client.post(f"/deliveries/{delivery['id']}/confirm")
    assert client.post(f"/deliveries/{delivery['id']}/confirm").status_code == 409
    res = client.post(f"/deliveries/{delivery['id']}/dispute", json={"farmer_kg": 12, "reason": "late"})
    assert res.status_code == 409


def test_dispute_requires_reason_and_weight(client, record):
    delivery = record(10).get_json()
    assert client.post(f"/deliveries/{delivery['id']}/dispute", json={"farmer_kg": 11}).status_code == 400
    assert client.post(f"/deliveries/{delivery['id']}/dispute", json={"reason": "x"}).status_code == 400


def test_list_deliveries_by_status(client, record):
    first = record(10).get_json()
    record(8)
    client.post(f"/deliveries/{first['id']}/confirm")
    assert len(client.get("/deliveries").get_json()) == 2
    assert len(client.get("/deliveries?status=pending").get_json()) == 1
    assert len(client.get("/deliveries?status=confirmed").get_json()) == 1
    assert client.get("/deliveries?status=lost").status_code == 400


def test_unknown_delivery_returns_404(client):
    assert client.get("/deliveries/123").status_code == 404
    assert client.post("/deliveries/123/confirm").status_code == 404


def test_dispute_report_groups_by_clerk(client, record):
    a = record(10, clerk="Otieno").get_json()
    b = record(9, clerk="Otieno").get_json()
    c = record(12, clerk="Chebet").get_json()
    client.post(f"/deliveries/{a['id']}/dispute", json={"farmer_kg": 11, "reason": "low"})
    client.post(f"/deliveries/{b['id']}/dispute", json={"farmer_kg": 9.5, "reason": "low"})
    client.post(f"/deliveries/{c['id']}/confirm")

    report = client.get("/reports/disputes").get_json()
    top = report[0]
    assert top["clerk"] == "Otieno"
    assert top["disputed"] == 2
    assert top["dispute_rate"] == 1.0
    assert top["kg_gap"] == 1.5
    assert report[1]["clerk"] == "Chebet"
    assert report[1]["disputed"] == 0
