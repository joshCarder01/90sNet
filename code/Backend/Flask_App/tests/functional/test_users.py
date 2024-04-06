"""
Testing users requests for correctness
"""
from Backend.Blueprints import users_blueprint
from Backend.Models import User

from .common import *

def test_users_get_all(test_client, test_data):
    """
    Test that when the `/users` page is accessed, it will get all of the users
    in the database.
    """
    
    response = test_client.get("/users")
    assert response.status_code == 200
    data: dict = response.json

    # Iterative Item Testing
    for user_check in test_data['users']:
        json_id = find_id_in_json(data, user_check.id)
        
        assert_all_values(data[json_id], user_check)

def test_users_post(test_client, user):

    new_user = user.serialize()
    resp = test_client.post('/users/add', json=new_user)

    assert resp.status_code == 200

    # Check the database
    data: (User | None) = User.query.filter_by(id = new_user['id']).scalar()

    assert data is not None

    assert_all_values(new_user, data)
