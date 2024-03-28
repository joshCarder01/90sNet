
import datetime
from typing import Union

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from Backend.Models import Event
from Backend import db
from . import events_blueprint
from Backend.common import HandleJSON


@events_blueprint.route("/events", methods=["GET", "POST"])
def get_all_events():
    """
    Expects no params, just gives all of the events
    """        

    # GET request, just return all of the events
    current_app.logger.debug("Begin /%s/ handling", events_blueprint.url_prefix)


    return jsonify(Event.serialize_list(db.session.execute(select(Event).order_by(Event.time)).scalars().all()))
    # return jsonify(db.session.execute(select(ScoreEvent).order_by(ScoreEvent.time)).scalars().all())

@events_blueprint.route('/getEventsSince', methods=['Get'])
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
    params: Union[None, dict] = request.json

    if params is None:
        return "No JSON Data", 400
    
    data = params.get('time', None)
    if data is None:
        return "Key time is missing", 400

    if not isinstance(params.get('time', None), (float)):
        return "Key time is not a float", 400

    # Gather the time argument
    time: datetime.datetime = datetime.datetime.fromtimestamp(params['time'])

    query = select(Event).where(Event.time > time).order_by(Event.time)
    
    data = db.session.execute(query).scalars().all()

    return jsonify(Event.serialize_list(data))

@events_blueprint.route("/events/add", methods=["POST"])
def add_event():
    if request.json:
        time = request.json.get('time', None)

        # Convert timestamp into datetime object
        if time is not None:
            time = datetime.datetime.fromtimestamp(time)
        new_event = Event(
            id=request.json.get('id', None),                    # Get id or use default
            type=request.json["type"],
            time=time,                                          # Get time or use default time.time
            machine_id=request.json['machine_id'],              # get machine id
            user_id=request.json.get("user_id", None),          # get user id or null
            description=request.json.get('description', None),  # get the description or null
        )
        db.session.add(new_event)
        db.session.commit()

        current_app.logger.debug(f"New event: {new_event.type} with {new_event.machine_id} - {new_event.user_id}")

        return jsonify(Event.serialize(new_event))
