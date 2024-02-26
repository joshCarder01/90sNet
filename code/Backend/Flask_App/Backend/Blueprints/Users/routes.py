
from flask import (
    jsonify, current_app
)
from sqlalchemy import select


from Backend.Models import User
from Backend import db
from . import users_blueprint


@users_blueprint.route("/getUsers", methods=["GET"])
def get_all():
    """
    Get all of the users in the database
    """
    current_app.logger.debug("Handling /%s/", users_blueprint.url_prefix)

    return jsonify(db.session.execute(select(User)).scalars().all())
