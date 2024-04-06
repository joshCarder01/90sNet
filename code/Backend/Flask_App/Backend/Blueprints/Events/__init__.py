from flask import Blueprint

events_blueprint = Blueprint("events", __name__)

from . import routes