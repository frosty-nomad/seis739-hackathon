from flask import request
from werkzeug.exceptions import BadRequest, NotFound

from ..extensions import db
from ..models import Guest, PartyList, RSVP_STATUSES


def get_json_payload():
    if not request.is_json:
        raise BadRequest("Request body must be JSON")
    return request.get_json()


def get_party_list_or_404(list_id):
    party_list = PartyList.query.get(list_id)
    if not party_list:
        raise NotFound("Party list not found")
    return party_list


def get_guest_or_404(guest_id):
    guest = Guest.query.get(guest_id)
    if not guest:
        raise NotFound("Guest not found")
    return guest


def normalize_rsvp_status(value):
    if value is None:
        return None
    status = str(value).strip().lower()
    if status not in RSVP_STATUSES:
        raise BadRequest(f"rsvp_status must be one of {', '.join(RSVP_STATUSES)}")
    return status
