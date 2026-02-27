from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from .extensions import db
from .models import Guest, PartyList, RSVP_STATUSES

api_bp = Blueprint("api", __name__)


def _get_json():
    if not request.is_json:
        raise BadRequest("Request body must be JSON")
    return request.get_json()


def _get_party_list_or_404(list_id):
    party_list = PartyList.query.get(list_id)
    if not party_list:
        raise NotFound("Party list not found")
    return party_list


def _get_guest_or_404(guest_id):
    guest = Guest.query.get(guest_id)
    if not guest:
        raise NotFound("Guest not found")
    return guest


def _normalize_rsvp_status(value):
    if value is None:
        return None
    status = str(value).strip().lower()
    if status not in RSVP_STATUSES:
        raise BadRequest(f"rsvp_status must be one of {', '.join(RSVP_STATUSES)}")
    return status


@api_bp.get("/lists")
def list_party_lists():
    lists = PartyList.query.order_by(PartyList.name).all()
    return jsonify([party_list.to_dict() for party_list in lists])


@api_bp.post("/lists")
def create_party_list():
    payload = _get_json()
    name = (payload.get("name") or "").strip()
    if not name:
        raise BadRequest("name is required")

    party_list = PartyList(name=name)
    db.session.add(party_list)
    db.session.commit()

    return jsonify(party_list.to_dict()), 201


@api_bp.get("/lists/<int:list_id>")
def get_party_list(list_id):
    party_list = _get_party_list_or_404(list_id)
    return jsonify(party_list.to_dict(include_guests=True))


@api_bp.put("/lists/<int:list_id>")
def update_party_list(list_id):
    party_list = _get_party_list_or_404(list_id)
    payload = _get_json()
    name = (payload.get("name") or "").strip()
    if not name:
        raise BadRequest("name is required")

    party_list.name = name
    db.session.commit()

    return jsonify(party_list.to_dict())


@api_bp.delete("/lists/<int:list_id>")
def delete_party_list(list_id):
    party_list = _get_party_list_or_404(list_id)
    db.session.delete(party_list)
    db.session.commit()
    return jsonify({"status": "deleted"})


@api_bp.get("/guests")
def list_guests():
    guests = Guest.query.order_by(Guest.name).all()
    return jsonify([guest.to_dict() for guest in guests])


@api_bp.post("/guests")
def create_guest():
    payload = _get_json()
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = _normalize_rsvp_status(payload.get("rsvp_status")) or "pending"
    if not name:
        raise BadRequest("name is required")

    guest = Guest(name=name, email=email, rsvp_status=rsvp_status)
    db.session.add(guest)
    db.session.commit()
    return jsonify(guest.to_dict()), 201


@api_bp.get("/guests/<int:guest_id>")
def get_guest(guest_id):
    guest = _get_guest_or_404(guest_id)
    return jsonify(guest.to_dict())


@api_bp.put("/guests/<int:guest_id>")
def update_guest(guest_id):
    guest = _get_guest_or_404(guest_id)
    payload = _get_json()
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = _normalize_rsvp_status(payload.get("rsvp_status"))
    if not name:
        raise BadRequest("name is required")

    guest.name = name
    guest.email = email
    if rsvp_status:
        guest.rsvp_status = rsvp_status
    db.session.commit()
    return jsonify(guest.to_dict())


@api_bp.delete("/guests/<int:guest_id>")
def delete_guest(guest_id):
    guest = _get_guest_or_404(guest_id)
    db.session.delete(guest)
    db.session.commit()
    return jsonify({"status": "deleted"})


@api_bp.get("/lists/<int:list_id>/guests")
def list_party_list_guests(list_id):
    party_list = _get_party_list_or_404(list_id)
    return jsonify([guest.to_dict() for guest in party_list.guests])


@api_bp.post("/lists/<int:list_id>/guests")
def add_guest_to_list(list_id):
    party_list = _get_party_list_or_404(list_id)
    payload = _get_json()

    guest_id = payload.get("guest_id")
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = _normalize_rsvp_status(payload.get("rsvp_status")) or "pending"

    if guest_id:
        guest = _get_guest_or_404(guest_id)
    elif name:
        guest = Guest(name=name, email=email, rsvp_status=rsvp_status)
        db.session.add(guest)
    else:
        raise BadRequest("guest_id or name is required")

    if guest not in party_list.guests:
        party_list.guests.append(guest)

    db.session.commit()
    return jsonify(party_list.to_dict(include_guests=True)), 201


@api_bp.delete("/lists/<int:list_id>/guests/<int:guest_id>")
def remove_guest_from_list(list_id, guest_id):
    party_list = _get_party_list_or_404(list_id)
    guest = _get_guest_or_404(guest_id)

    if guest in party_list.guests:
        party_list.guests.remove(guest)
        db.session.commit()

    return jsonify(party_list.to_dict(include_guests=True))
