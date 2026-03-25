from flask import jsonify
from werkzeug.exceptions import BadRequest

from . import api_bp
from .common import db, get_guest_or_404, get_json_payload, normalize_rsvp_status
from ..models import Guest


@api_bp.get("/guests")
def list_guests():
    guests = Guest.query.order_by(Guest.name).all()
    return jsonify([guest.to_dict() for guest in guests])


@api_bp.post("/guests")
def create_guest():
    payload = get_json_payload()
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = normalize_rsvp_status(payload.get("rsvp_status")) or "pending"
    if not name:
        raise BadRequest("name is required")

    guest = Guest(name=name, email=email, rsvp_status=rsvp_status)
    db.session.add(guest)
    db.session.commit()
    return jsonify(guest.to_dict()), 201


@api_bp.get("/guests/<int:guest_id>")
def get_guest(guest_id):
    guest = get_guest_or_404(guest_id)
    return jsonify(guest.to_dict())


@api_bp.put("/guests/<int:guest_id>")
def update_guest(guest_id):
    guest = get_guest_or_404(guest_id)
    payload = get_json_payload()
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip() or None
    rsvp_status = normalize_rsvp_status(payload.get("rsvp_status"))
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
    guest = get_guest_or_404(guest_id)
    db.session.delete(guest)
    db.session.commit()
    return jsonify({"status": "deleted"})
