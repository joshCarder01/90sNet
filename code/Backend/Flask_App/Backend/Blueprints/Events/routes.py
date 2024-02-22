
import datetime

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from Backend.Models import ScoreEvent
from Backend import db
from . import events_blueprint


@events_blueprint.route("/", methods=["GET"])
def get_all_events():
    """
    Expects no params, just gives all of the events
    """

    current_app.logger.debug("Begin /{}/ handling", events_blueprint.url_prefix)

    return jsonify(db.session.query(ScoreEvent).all())

@events_blueprint.route('/since', methods=['Get'])
def get_events_since():
    """
    Expecting params json as follows:
    {
        "time": {{Time to get events since}}
    }

    Raises 415 Media Type not Supported if not `Content-Type: application/json`
    """

    current_app.logger.debug("Begin /{}/since handling", events_blueprint.url_prefix)
    # Begin handling the event
    params = request.json()

    # Gather the time argument
    time: datetime.datetime = datetime.datetime.fromtimestamp(params['time'], datetime.UTC)

    query = select(ScoreEvent).where(ScoreEvent.time >= time).order_by(ScoreEvent.time)
    data = db.session.execute(query)

    return jsonify(data)