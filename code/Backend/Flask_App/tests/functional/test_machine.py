"""
Testing requests to machine api gets the correct response
"""
from .common import *
from Backend.Blueprints import machines_blueprint
from Backend.Models import Machine

def test_AS6_machines_get_all(test_client, test_data):
    """
    Test that when the `/machines` page is accessed, it will get all of the users
    in the database.
    """
    response = test_client.get("/machines")
    assert response.status_code == 200

    data: dict | None = response.json
    assert data is not None

    # Iterative Item Testing
    for machine_check in test_data['machines']:
        json_id = find_id_in_json(data, machine_check.id)

        assert_all_values(machine_check, data[json_id])


def test_AS7_machines_post(test_client, machine):
    new_machine = machine.serialize()

    response = test_client.post("/machines/add", json=new_machine)

    assert response.status_code == 200

    data: (Machine | None) = Machine.query.filter_by(id = new_machine["id"]).scalar()
    
    assert data is not None

    assert_all_values(new_machine, data)
