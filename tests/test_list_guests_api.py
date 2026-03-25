def test_list_guests_for_party_list_empty(client):
    create_list_response = client.post("/api/lists", json={"name": "Event"})
    list_id = create_list_response.get_json()["id"]

    response = client.get(f"/api/lists/{list_id}/guests")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_existing_guest_to_list(client):
    create_list_response = client.post("/api/lists", json={"name": "Wedding"})
    list_id = create_list_response.get_json()["id"]

    create_guest_response = client.post("/api/guests", json={"name": "Alex"})
    guest_id = create_guest_response.get_json()["id"]

    response = client.post(f"/api/lists/{list_id}/guests", json={"guest_id": guest_id})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == list_id
    assert len(data["guests"]) == 1
    assert data["guests"][0]["id"] == guest_id


def test_add_new_guest_to_list_by_name(client):
    create_list_response = client.post("/api/lists", json={"name": "Birthday"})
    list_id = create_list_response.get_json()["id"]

    response = client.post(
        f"/api/lists/{list_id}/guests",
        json={"name": "Sam", "email": "sam@example.com", "rsvp_status": "pending"},
    )
    assert response.status_code == 201
    guests = response.get_json()["guests"]
    assert len(guests) == 1
    assert guests[0]["name"] == "Sam"


def test_add_guest_to_list_requires_guest_id_or_name(client):
    create_list_response = client.post("/api/lists", json={"name": "Conference"})
    list_id = create_list_response.get_json()["id"]

    response = client.post(f"/api/lists/{list_id}/guests", json={})
    assert response.status_code == 400


def test_remove_guest_from_list(client):
    create_list_response = client.post("/api/lists", json={"name": "Dinner"})
    list_id = create_list_response.get_json()["id"]

    create_guest_response = client.post("/api/guests", json={"name": "Jordan"})
    guest_id = create_guest_response.get_json()["id"]

    client.post(f"/api/lists/{list_id}/guests", json={"guest_id": guest_id})
    remove_response = client.delete(f"/api/lists/{list_id}/guests/{guest_id}")

    assert remove_response.status_code == 200
    assert remove_response.get_json()["guests"] == []
