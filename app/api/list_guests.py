from flask import jsonify
from werkzeug.exceptions import BadRequest

from . import api_bp
from .common import (
    db,
    get_guest_or_404,
    get_json_payload,
    get_party_list_or_404,
    normalize_rsvp_status,
)
from ..models import Guest


@api_bp.get("/lists/<int:list_id>/guests")
def list_party_list_guests(list_id):
    party_list = get_party_list_or_404(list_id)
    return jsonify([guest.to_dict() for guest in party_list.guests])


@api_bp.post("/lists/<int:list_id>/guests")
def add_guest_to_list(list_id):
    party_list = get_party_list_or_404(list_id)
    payload = get_json_payload()

    guest_id = payload.get("guest_id")
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = normalize_rsvp_status(payload.get("rsvp_status")) or "pending"

    if guest_id:
        guest = get_guest_or_404(guest_id)
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
    party_list = get_party_list_or_404(list_id)
    guest = get_guest_or_404(guest_id)

    if guest in party_list.guests:
        party_list.guests.remove(guest)
        db.session.commit()

    return jsonify(party_list.to_dict(include_guests=True))
