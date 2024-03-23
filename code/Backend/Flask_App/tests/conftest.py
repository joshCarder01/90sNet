from flask_sqlalchemy import SQLAlchemy
import pytest
import os

from datetime import datetime, UTC
from flask import Flask

from Backend import create_app, db as _db

from Backend.Models.seeder import Seeder

@pytest.fixture(scope="session", autouse=True)
def app():
    # Set the testing config to be the class config to be utilized
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(app):

    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture(scope="module")
def base_time():
    return datetime(2024, 1, 1, 12, 0, 0, 0, UTC)

@pytest.fixture(scope='session', autouse=True)
def db(app: Flask, request: pytest.FixtureRequest):
    if os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
        os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])

    _db.create_all()

    def teardown():
        _db.drop_all()
        try:
            os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])
        except OSError:
            pass
    
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db: SQLAlchemy, request: pytest.FixtureRequest):
    """
    Creates a session which is scoped to this pytest
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)
    
    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()
    
    request.addfinalizer(teardown)
    return session
    


@pytest.fixture(scope="module")
def test_data():

    correctness_tester = Seeder.SeedTestDatabase()

    return correctness_tester


@pytest.fixture(scope='function')
def user():
    user = Seeder.user_factory()
    assert not isinstance(user, list)
    return user

@pytest.fixture(scope="function")
def machine():
    machine = Seeder.machine_factory()
    assert not isinstance(machine, list)
    return machine

@pytest.fixture(scope="function")
def event(session, user, machine):
    session.add(user)
    session.add(machine)
    session.commit()
    
    event = Seeder.event_factory()

    assert not isinstance(event, list)
    return event

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
