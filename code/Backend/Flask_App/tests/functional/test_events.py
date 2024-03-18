"""
Testing requests to machine api gets the correct response
"""
import pytest
import logging
from typing import List

from .common import find_id_in_json
from Backend.Blueprints import events_blueprint
from Backend.Models import Event
from Backend import db

LOGGER = logging.getLogger(__name__)


def test_events_get_all(test_client, init_database):
    """
    Test that when the `/events` page is accessed, it will get all of the users
    in the database.
    """
    response = test_client.get("/events")
    assert response.status_code == 200

    data: List[dict] = response.json
    # Iterative Item Testing
    for event_check in init_database['events']:
        json_id = find_id_in_json(data, event_check.id)
        assert data[json_id]['id'] == event_check.id
        assert data[json_id]['time'] == event_check.timestamp
        assert data[json_id]['user_id'] == event_check.user_id
        assert data[json_id]['machine_id'] == event_check.machine_id

def test_events_get_since(test_client, init_database):
    """
    Test the correct events are returned for each different time.
    """

    # loop through each event to set up a time
    for i in range(len(init_database['events'])):
        request_json = {'time': init_database['events'][i].timestamp}

        # Send request
        response = test_client.get("/getEventsSince", json=request_json)
        assert response.status_code == 200

        data: List[dict] = response.json

        # First check that items up to that since time is not in the response
        for j in range(i):
            event_check = init_database['events'][j]
            print("Looking for:", event_check.id)
            print("Data:", str(data))
            with pytest.raises(KeyError):
                find_id_in_json(data, event_check.id)
        
        # Now check the rest of the data is actually there
        for j in range(i+1, len(init_database['events'])):
            event_check = init_database['events'][j]
            json_id = find_id_in_json(data, event_check.id)
            assert data[json_id]['id'] == event_check.id
            assert data[json_id]['time'] == event_check.timestamp
            assert data[json_id]['user_id'] == event_check.user_id
            assert data[json_id]['machine_id'] == event_check.machine_id
1
def test_events_post(test_client, init_database):

    new_event = {"id": 4404, "type": "score", "user_id": init_database['users'][0].id, "machine_id": init_database['machines'][0].id}
    resp = test_client.post("/events/add", json=new_event)
    
    # Should just get the status_code
    assert resp.status_code == 200

    # Now we need to check that has actually been added to the database
    data = Event.query.filter_by(id = new_event['id']).scalar()

    assert data is not None
    assert data.id == new_event['id']
    assert data.type.name == new_event['type']
    assert data.machine_id == new_event['machine_id']
    assert data.user_id == new_event['user_id']

