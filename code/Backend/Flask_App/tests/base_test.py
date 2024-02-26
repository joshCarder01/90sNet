import pytest

from datetime import datetime, timedelta

from Backend import create_app, db

from Backend.Models import User, Machine, ScoreEvent

@pytest.fixture()
def app():
    app = create_app()

    # Set up app to be in testing mode
    app.config.update({
        "TESTING": True
    })

    # Add more as needed

    yield app

    # Add any cleanup which is needed

@pytest.fixutre(scope="module")
def base_time():
    return datetime(2024, 1, 1, 12, 0, 0, 0, datetime.UTC)

@pytest.fixture(scope="module")
def event_times(base_time):
    """
    Give the different times for the events
    """
    return (
        base_time,
        base_time+timedelta(minutes=1, seconds=5),
        base_time+timedelta(minutes=2, seconds=3),
        base_time+timedelta(hours=1)
    )

@pytest.fixture(scope="module")
def init_database(event_times):
    

    # Create the initial Database
    db.create_all()

    # Setting up some test users
    users = (
        User(453, "testuser1", "User Name 1"),
        User(454, "testuser2"),
        User(455, "testuser3", "User Name 3")
    )

    db.session.add_all(users)

    # Setting up test machines
    machines = (
        Machine(1001, "machine1", 500),
        Machine(1002, "machine2", 800),
        Machine(1003, "machine3", 1000)
    )

    db.session.add_all(machines)


    # Setting up score events
    events = (
        ScoreEvent(201, event_times[0], users[0].id, machines[0].id),
        ScoreEvent(202, event_times[1], users[0].id, machines[1].id),
        ScoreEvent(203, event_times[2], users[1].id, machines[1].id),
        ScoreEvent(204, event_times[3], users[2].id, machines[2].id)
    )

    db.session.add_all(events)

    # Commit the database
    db.session.commit()

    # Object given to the test which contains all the correct values of the database
    correctness_tester = {
        "users": users,
        "machines": machines,
        "events": events
    }

    yield correctness_tester

    # Discard changes

    db.drop_all()




@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
