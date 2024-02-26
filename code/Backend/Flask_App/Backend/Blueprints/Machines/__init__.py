from flask import Blueprint

machines_blueprint = Blueprint("machines", __name__, url_prefix="/machines")

from . import routes