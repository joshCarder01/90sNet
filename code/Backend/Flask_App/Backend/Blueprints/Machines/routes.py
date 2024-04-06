
import datetime

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from Backend.Models import Machine
from Backend import db
from Backend.common import HandleJSON
from . import machines_blueprint


@machines_blueprint.route("/machines", methods=["GET"])
def get_all_machines():
    """
    Expects no params, just gives all of the machines
    """

    current_app.logger.debug("Begin /%s/ handling", "machines")

    return jsonify(db.session.execute(select(Machine)).scalars().all())


@machines_blueprint.route("/machines/add", methods=["POST"])
def add_machine():
    if request.json:

        with HandleJSON():
            new_machine = Machine(
                id = request.json.get('id', None),
                name = request.json["name"],
                location = request.json['location']
            )


        db.session.add(new_machine)
        db.session.commit()

        current_app.logger.info(f"New Machine: {str(new_machine)}")

        return jsonify(new_machine)
    else:
        return "Must post json data", 400