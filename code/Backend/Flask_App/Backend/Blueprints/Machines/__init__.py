from flask import Blueprint

machines_blueprint = Blueprint("machines", __name__)

from . import routes