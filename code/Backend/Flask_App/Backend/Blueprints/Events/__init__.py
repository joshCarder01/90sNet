from flask import Blueprint

events_blueprint = Blueprint("events", __name__, url_prefix="/events")

from . import routes