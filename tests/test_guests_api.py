
def test_list_guests_empty(client):
    response = client.get("/api/guests")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_guest_success(client):
    response = client.post(
        "/api/guests",
        json={"name": "Alice", "email": "alice@example.com", "rsvp_status": "accepted"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["rsvp_status"] == "accepted"


def test_create_guest_requires_name(client):
    response = client.post("/api/guests", json={"email": "no-name@example.com"})
    assert response.status_code == 400


def test_create_guest_invalid_rsvp_status(client):
    response = client.post("/api/guests", json={"name": "Bob", "rsvp_status": "maybe"})
    assert response.status_code == 400


def test_get_guest_success(client):
    create_response = client.post("/api/guests", json={"name": "Carol"})
    guest_id = create_response.get_json()["id"]

    response = client.get(f"/api/guests/{guest_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == guest_id


def test_get_guest_not_found(client):
    response = client.get("/api/guests/9999")
    assert response.status_code == 404


def test_update_guest_success(client):
    create_response = client.post("/api/guests", json={"name": "Dave"})
    guest_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/api/guests/{guest_id}",
        json={"name": "David", "email": "david@example.com", "rsvp_status": "declined"},
    )
    assert update_response.status_code == 200
    data = update_response.get_json()
    assert data["name"] == "David"
    assert data["email"] == "david@example.com"
    assert data["rsvp_status"] == "declined"


def test_delete_guest_success(client):
    create_response = client.post("/api/guests", json={"name": "Erin"})
    guest_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/api/guests/{guest_id}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["status"] == "deleted"

    get_response = client.get(f"/api/guests/{guest_id}")
    assert get_response.status_code == 404
