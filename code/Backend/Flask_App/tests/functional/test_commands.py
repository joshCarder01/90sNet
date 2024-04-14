def test_AS1_command_blank(test_client, redis_clear):
    response = test_client.get("/command")

    assert response.status_code == 200
    assert response.data == b'null\n'


def test_AS2_command_transaction(test_client, redis_clear):

    test_commands = [
        {
            "cmd": "up",
            "args": [
                "some",
                "args"
            ]
        },
        {
            "cmd": "down",
            "args": [
                "many",
                "args"
            ]
        }
    ]

    for i in range(0, len(test_commands)):
        response = test_client.post("/command", json=test_commands[i])

        assert response.status_code == 200
        assert response.json is not None
        assert 'id' in response.json.keys()

        test_commands[i]['id'] = response.json['id']
    
    # Now we need to know those commands actually complete
    for i in range(0, len(test_commands)):
        response = test_client.get("/command")

        assert response.status_code == 200

        assert response.json == test_commands[i]
    
    # Now should begin returning blanks again
    response = test_client.get("/command")

    assert response.status_code == 200
    assert response.data == b'null\n'
