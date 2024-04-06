
from flask import (
    jsonify, current_app, request
)
from sqlalchemy import select


from Backend.Models import User
from Backend import db
from Backend.common import HandleJSON
from . import users_blueprint


@users_blueprint.route("/users", methods=["GET"])
def get_all():
    """
    Get all of the users in the database
    """
    current_app.logger.debug("Handling /%s/", "users")

    return jsonify(db.session.execute(select(User)).scalars().all())

@users_blueprint.post("/users/add")
def add_user():

    with HandleJSON():
        new_user = User(
            id = request.json.get('id', None),
            name = request.json.get("name", None),
            username=request.json['username']
        )
        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info(f"New User: {str(new_user)}")

        return jsonify(new_user)
