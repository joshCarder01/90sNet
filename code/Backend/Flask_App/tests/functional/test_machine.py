"""
Testing requests to machine api gets the correct response
"""
from .common import find_id_in_json
from Backend.Blueprints import machines_blueprint
from Backend.Models import Machine

def test_machines_get_all(test_client, init_database):
    """
    Test that when the `/machines` page is accessed, it will get all of the users
    in the database.
    """
    response = test_client.get("/machines")
    assert response.status_code == 200

    data: dict = response.json
    # Iterative Item Testing
    for machine_check in init_database['machines']:
        json_id = find_id_in_json(data, machine_check.id)
        assert data[json_id]['id'] == machine_check.id
        assert data[json_id]['score'] == machine_check.score
        assert data[json_id]['name'] == machine_check.name

def test_machines_post(test_client, init_database):
    new_machine = {"id": 402934, "name": "some_new_machine", "score": 500}
    response = test_client.post("/machines/add", json=new_machine)

    assert response.status_code == 200

    data: (Machine | None) = Machine.query.filter_by(id = new_machine["id"]).scalar()
    
    assert data is not None
    assert data.id == new_machine['id']
    assert data.name == new_machine["name"]
    assert data.score == new_machine["score"]
