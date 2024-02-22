
import datetime

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from Backend.Models import Machine
from Backend import db
from . import machines_blueprint


@machines_blueprint.route("/", methods=["GET"])
def get_all_machines():
    """
    Expects no params, just gives all of the machines
    """

    current_app.logger.debug("Begin /{}/ handling", machines_blueprint.url_prefix)

    return jsonify(db.session.query(Machine).all())
