from app.extensions import db
from app.models import PartyList


def test_list_party_lists_empty(client):
    response = client.get("/api/lists")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_party_list_success(client):
    response = client.post("/api/lists", json={"name": "Family"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Family"
    assert "id" in data


def test_create_party_list_requires_name(client):
    response = client.post("/api/lists", json={})
    assert response.status_code == 400


def test_get_party_list_success(client):
    create_response = client.post("/api/lists", json={"name": "Friends"})
    list_id = create_response.get_json()["id"]

    response = client.get(f"/api/lists/{list_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == list_id
    assert data["name"] == "Friends"


def test_get_party_list_not_found(client):
    response = client.get("/api/lists/9999")
    assert response.status_code == 404


def test_update_party_list_success(client):
    create_response = client.post("/api/lists", json={"name": "Old Name"})
    list_id = create_response.get_json()["id"]

    response = client.put(f"/api/lists/{list_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "New Name"


def test_update_party_list_requires_name(client):
    create_response = client.post("/api/lists", json={"name": "To Update"})
    list_id = create_response.get_json()["id"]

    response = client.put(f"/api/lists/{list_id}", json={})
    assert response.status_code == 400


def test_delete_party_list_success(client):
    create_response = client.post("/api/lists", json={"name": "Delete Me"})
    list_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/api/lists/{list_id}")
    assert delete_response.status_code == 200
    assert delete_response.get_json()["status"] == "deleted"

    get_response = client.get(f"/api/lists/{list_id}")
    assert get_response.status_code == 404
