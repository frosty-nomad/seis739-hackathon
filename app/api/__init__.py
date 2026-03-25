from flask import Blueprint

api_bp = Blueprint("api", __name__)

# Import endpoint modules so route decorators are registered on the blueprint.
from . import guests, list_guests, lists  # noqa: E402,F401
