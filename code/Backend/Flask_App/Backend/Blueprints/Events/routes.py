
import datetime

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from Backend.Models import ScoreEvent
from Backend import db
from . import events_blueprint


@events_blueprint.route("/", methods=["GET"])
@events_blueprint.route("", methods=["GET"])
def get_all_events():
    """
    Expects no params, just gives all of the events
    """

    current_app.logger.debug("Begin /%s/ handling", events_blueprint.url_prefix)


    # return jsonify(ScoreEvent.serialize_list(db.session.execute(select(ScoreEvent).order_by(ScoreEvent.time)).scalars().all()))
    return jsonify(db.session.execute(select(ScoreEvent).order_by(ScoreEvent.time)).scalars().all())

@events_blueprint.route('/since', methods=['Get'])
def get_events_since():
    """
    Expecting params json as follows:
    {
        "time": {{Time to get events since}}
    }

    Raises 415 Media Type not Supported if not `Content-Type: application/json`
    """

    current_app.logger.debug("Begin /%s/since handling", events_blueprint.url_prefix)
    # Begin handling the event
    params = request.json

    if params is None:
        return "No JSON Data", 400
    
    if not 'time' in params:
        return "Key time is missing", 400

    # Gather the time argument
    time: datetime.datetime = datetime.datetime.fromtimestamp(params['time'], datetime.UTC)

    query = select(ScoreEvent).where(ScoreEvent.time > time).order_by(ScoreEvent.time)
    
    data = db.session.execute(query).scalars().all()

    return jsonify(ScoreEvent.serialize_list(data))
