from .extensions import db

party_list_guests = db.Table(
    "party_list_guests",
    db.Column("party_list_id", db.Integer, db.ForeignKey("party_lists.id"), primary_key=True),
    db.Column("guest_id", db.Integer, db.ForeignKey("guests.id"), primary_key=True),
)

RSVP_STATUSES = ("pending", "accepted", "declined")


class PartyList(db.Model):
    __tablename__ = "party_lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    guests = db.relationship(
        "Guest",
        secondary=party_list_guests,
        back_populates="party_lists",
        order_by="Guest.name",
    )

    def to_dict(self, include_guests=False):
        data = {
            "id": self.id,
            "name": self.name,
            "guest_count": len(self.guests),
        }
        if include_guests:
            data["guests"] = [guest.to_dict() for guest in self.guests]
        return data


class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255))
    rsvp_status = db.Column(db.String(16), nullable=False, default="pending")
    party_lists = db.relationship(
        "PartyList",
        secondary=party_list_guests,
        back_populates="guests",
        order_by="PartyList.name",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "rsvp_status": self.rsvp_status,
        }
