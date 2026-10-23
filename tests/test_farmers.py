def test_create_and_list_centres(client):
    res = client.post("/centres", json={"name": "Litein Buying Centre", "county": "Kericho"})
    assert res.status_code == 201
    assert res.get_json()["name"] == "Litein Buying Centre"
    assert len(client.get("/centres").get_json()) == 1


def test_duplicate_centre_is_rejected(client, centre):
    res = client.post("/centres", json={"name": centre["name"], "county": "Kisii"})
    assert res.status_code == 409


def test_register_farmer_assigns_number_and_normalises_phone(farmer):
    assert farmer["farmer_no"] == "CL-0001"
    assert farmer["phone"] == "+254712345678"
    assert farmer["centre_name"] == "Kiamokama Buying Centre"


def test_farmer_numbers_increment(client, centre, farmer):
    second = client.post(
        "/farmers", json={"name": "John Kiprono", "phone": "0722000111", "centre_id": centre["id"]}
    ).get_json()
    assert second["farmer_no"] == "CL-0002"


def test_duplicate_phone_is_rejected(client, centre, farmer):
    res = client.post(
        "/farmers", json={"name": "Someone Else", "phone": "+254712345678", "centre_id": centre["id"]}
    )
    assert res.status_code == 409


def test_farmer_needs_existing_centre(client):
    res = client.post("/farmers", json={"name": "Mary", "phone": "0712345678", "centre_id": 99})
    assert res.status_code == 404


def test_farmer_validation_errors(client, centre):
    assert client.post("/farmers", json={"phone": "0712345678", "centre_id": centre["id"]}).status_code == 400
    assert client.post("/farmers", json={"name": "A", "phone": "123", "centre_id": centre["id"]}).status_code == 400
    assert client.post("/farmers", data="not json").status_code == 400


def test_get_and_filter_farmers(client, centre, farmer):
    assert client.get(f"/farmers/{farmer['id']}").get_json()["name"] == "Mary Wanjiku"
    assert client.get("/farmers/999").status_code == 404
    assert len(client.get(f"/farmers?centre_id={centre['id']}").get_json()) == 1
