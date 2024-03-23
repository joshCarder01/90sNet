"""
Testing requests to machine api gets the correct response
"""
from flask import Flask
import pytest
import logging
from typing import List

from .common import *
from Backend.Models import Event

LOGGER = logging.getLogger(__name__)


def test_events_get_all(test_client, test_data):
    """
    Test that when the `/events` page is accessed, it will get all of the users
    in the database.
    """
    response = test_client.get("/events")
    assert response.status_code == 200

    data: List[dict] = response.json
    # Iterative Item Testing
    for event_check in test_data['events']:
        json_id = find_id_in_json(data, event_check.id)
        assert_all_values(data[json_id], event_check)

def test_events_get_since(test_client, test_data):
    """
    Test the correct events are returned for each different time.
    """

    # loop through each event to set up a time
    for i in range(len(test_data['events'])):
        request_json = {'time': test_data['events'][i].timestamp}

        # Send request
        response = test_client.get("/getEventsSince", json=request_json)
        assert response.status_code == 200

        data: List[dict] = response.json

        # First check that items up to that since time is not in the response
        for j in range(i):
            event_check = test_data['events'][j]
            print("Looking for:", event_check.id)
            print("Data:", str(data))
            with pytest.raises(KeyError):
                find_id_in_json(data, event_check.id)
        
        # Now check the rest of the data is actually there
        for j in range(i+1, len(test_data['events'])):
            event_check = test_data['events'][j]
            json_id = find_id_in_json(data, event_check.id)

            assert_all_values(data[json_id], event_check)

def test_events_post(test_client: Flask, event):
    new_event = event.serialize()
    print(new_event)
    resp = test_client.post("/events/add", json=new_event)

    
    # Should just get the status_code
    assert resp.status_code == 200

    # Now we need to check that has actually been added to the database
    data = Event.query.filter_by(id = new_event['id']).scalar()

    assert data is not None

    assert_all_values(new_event, data)

