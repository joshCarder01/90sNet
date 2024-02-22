
from flask import (
    jsonify, current_app
)

from Backend.Models import User
from Backend import db
from . import users_blueprint


@users_blueprint.route("/", method=["GET"])
def get_all_users():
    """
    Get all of the users in the database
    """
    current_app.logger.debug("Handling /{}/", users_blueprint.url_prefix)

    return jsonify(db.session.query(User).all())
