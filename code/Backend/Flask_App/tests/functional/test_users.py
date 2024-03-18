"""
Testing users requests for correctness
"""
from Backend.Blueprints import users_blueprint
from Backend.Models import User

from .common import find_id_in_json

def test_users_get_all(test_client, init_database):
    """
    Test that when the `/users` page is accessed, it will get all of the users
    in the database.
    """
    
    response = test_client.get("/users")
    assert response.status_code == 200
    data: dict = response.json

    # Iterative Item Testing
    for user_check in init_database['users']:
        json_id = find_id_in_json(data, user_check.id)
        assert data[json_id]['id'] == user_check.id
        assert data[json_id]['username'] == user_check.username
        assert data[json_id]['name'] == user_check.name

def test_users_post(test_client, init_database):

    new_user = {"id": 40289, "username": "some_new_user", "name": "This_Name"}
    resp = test_client.post('/users/add', json=new_user)

    assert resp.status_code == 200

    # Check the database
    data: (User | None) = User.query.filter_by(id = new_user['id']).scalar()

    assert data is not None
    assert data.id == new_user['id']
    assert data.username == new_user['username']
    assert data.name == new_user['name']
