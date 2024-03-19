import pytest
import os

from datetime import datetime, timedelta, UTC
from typing import Dict, Union, Tuple

from Backend import create_app, db

from Backend.Models import User, Machine, Event
from Backend.Models.seeder import Seeder

@pytest.fixture(scope='module')
def test_client():
    # Set the testing config to be the class config to be utilized
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture(scope="module")
def base_time():
    return datetime(2024, 1, 1, 12, 0, 0, 0, UTC)

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
    

    db.drop_all()
    # Create the initial Database
    db.create_all()

    correctness_tester = Seeder.SeedTestDatabase()

    # # Setting up some test users
    # users = (
    #     User(id=453, username="testuser0",  name="User Name 0"),
    #     User(id=454, username="testuser1"),
    #     User(id=455, username="testuser2",  name="User Name 2")
    # )

    # db.session.add_all(users)

    # # Setting up test machines
    # machines = (
    #     Machine(id=1001, name="machine0", score=500),
    #     Machine(id=1002, name="machine1", score=800),
    #     Machine(id=1003, name="machine2", score=1000)
    # )

    # db.session.add_all(machines)


    # # Setting up score events
    # events = (
    #     ScoreEvent(id=201, time=event_times[0], user_id=users[0].id, machine_id=machines[0].id),
    #     ScoreEvent(id=202, time=event_times[1], user_id=users[0].id, machine_id=machines[1].id),
    #     ScoreEvent(id=203, time=event_times[2], user_id=users[1].id, machine_id=machines[1].id),
    #     ScoreEvent(id=204, time=event_times[3], user_id=users[2].id, machine_id=machines[2].id)
    # )

    # db.session.add_all(events)

    # # Commit the database
    # db.session.commit()

    # Object given to the test which contains all the correct values of the database
    # correctness_tester: Dict[str, Union[Tuple[User], Tuple[Machine], Tuple[ScoreEvent]]] = {
    #     "users": users,
    #     "machines": machines,
    #     "events": events
    # }

    return correctness_tester

    




@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
