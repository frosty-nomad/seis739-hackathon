from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.exceptions import BadRequest

from .extensions import db
from .models import Guest, PartyList, RSVP_STATUSES

web_bp = Blueprint("web", __name__)


def _require_name(value):
    name = (value or "").strip()
    if not name:
        raise BadRequest("Name is required")
    return name


@web_bp.get("/")
def index():
    lists = PartyList.query.order_by(PartyList.name).all()
    return render_template("index.html", lists=lists)


@web_bp.post("/lists")
def create_list():
    name = _require_name(request.form.get("name"))
    party_list = PartyList(name=name)
    db.session.add(party_list)
    db.session.commit()
    return redirect(url_for("web.index"))


@web_bp.post("/lists/<int:list_id>/delete")
def delete_list(list_id):
    party_list = PartyList.query.get_or_404(list_id)
    db.session.delete(party_list)
    db.session.commit()
    return redirect(url_for("web.index"))


@web_bp.get("/lists/<int:list_id>")
def list_detail(list_id):
    party_list = PartyList.query.get_or_404(list_id)
    return render_template(
        "list_detail.html",
        party_list=party_list,
        rsvp_options=RSVP_STATUSES,
    )


@web_bp.post("/lists/<int:list_id>/guests")
def add_guest(list_id):
    party_list = PartyList.query.get_or_404(list_id)
    name = _require_name(request.form.get("name"))
    email = (request.form.get("email") or "").strip() or None
    rsvp_status = (request.form.get("rsvp_status") or "pending").strip().lower()
    if rsvp_status not in RSVP_STATUSES:
        raise BadRequest("Invalid RSVP status")

    guest = Guest(name=name, email=email, rsvp_status=rsvp_status)
    party_list.guests.append(guest)
    db.session.add(guest)
    db.session.commit()

    return redirect(url_for("web.list_detail", list_id=list_id))


@web_bp.post("/lists/<int:list_id>/guests/<int:guest_id>/rsvp")
def update_rsvp(list_id, guest_id):
    party_list = PartyList.query.get_or_404(list_id)
    guest = Guest.query.get_or_404(guest_id)
    rsvp_status = (request.form.get("rsvp_status") or "").strip().lower()
    if rsvp_status not in RSVP_STATUSES:
        raise BadRequest("Invalid RSVP status")

    if guest in party_list.guests:
        guest.rsvp_status = rsvp_status
        db.session.commit()

    return redirect(url_for("web.list_detail", list_id=list_id))


@web_bp.post("/lists/<int:list_id>/guests/<int:guest_id>/delete")
def remove_guest(list_id, guest_id):
    party_list = PartyList.query.get_or_404(list_id)
    guest = Guest.query.get_or_404(guest_id)

    if guest in party_list.guests:
        party_list.guests.remove(guest)
        db.session.commit()

    return redirect(url_for("web.list_detail", list_id=list_id))
