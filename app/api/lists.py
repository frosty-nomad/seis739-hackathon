from flask import jsonify
from werkzeug.exceptions import BadRequest

from . import api_bp
from .common import db, get_json_payload, get_party_list_or_404
from ..models import PartyList


@api_bp.get("/lists")
def list_party_lists():
    lists = PartyList.query.order_by(PartyList.name).all()
    return jsonify([party_list.to_dict() for party_list in lists])


@api_bp.post("/lists")
def create_party_list():
    payload = get_json_payload()
    name = (payload.get("name") or "").strip()
    if not name:
        raise BadRequest("name is required")

    party_list = PartyList(name=name)
    db.session.add(party_list)
    db.session.commit()

    return jsonify(party_list.to_dict()), 201


@api_bp.get("/lists/<int:list_id>")
def get_party_list(list_id):
    party_list = get_party_list_or_404(list_id)
    return jsonify(party_list.to_dict(include_guests=True))


@api_bp.put("/lists/<int:list_id>")
def update_party_list(list_id):
    party_list = get_party_list_or_404(list_id)
    payload = get_json_payload()
    name = (payload.get("name") or "").strip()
    if not name:
        raise BadRequest("name is required")

    party_list.name = name
    db.session.commit()

    return jsonify(party_list.to_dict())


@api_bp.delete("/lists/<int:list_id>")
def delete_party_list(list_id):
    party_list = get_party_list_or_404(list_id)
    db.session.delete(party_list)
    db.session.commit()
    return jsonify({"status": "deleted"})
