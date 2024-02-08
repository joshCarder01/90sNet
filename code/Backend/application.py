# Package imports
from .database import DBManager

# Other imports

import flask
import datetime

# Flask because why not rest
app = flask.Flask("90snet_backend")

manager = DBManager




@app.route('/pwn_events', methods=['Get'])
def get_pwn_events():
    """
    Expecting params json as follows:
    {
        "time": {{Time to get events since}}
    }
    """
    # Begin handling the event
    params = flask.request

    # Gather the time argument
    time: datetime.datetime = datetime.datetime.fromtimestamp(params['time'], datetime.UTC)

    data = manager.events_since(time)

    return flask.jsonify(data)
    

# Use this on the native application side.
if __name__ == "__main__":
    manager.create_db("./db/testing.sqlite")
    
    

