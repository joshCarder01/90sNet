from flask_sqlalchemy import SQLAlchemy
import pytest
import os

import sqlalchemy as sa

from datetime import datetime, UTC
from flask import Flask
from sqlalchemy.orm import Session

from Backend import create_app, db as _db
from config import TestingConfig
from Backend.Models.seeder import Seeder

@pytest.fixture(scope="session", autouse=True)
def app(request: pytest.FixtureRequest):
    # Set the testing config to be the class config to be utilized
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    ctx = app.app_context()
    ctx.push()
    
    def teardown():
        ctx.pop()
    
    request.addfinalizer(teardown)
    return app

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

    path = app.config['SQLALCHEMY_DATABASE_URI'][10:]

    _db.drop_all()
    _db.create_all()

    yield _db

    _db.drop_all()
    os.unlink(path)


@pytest.fixture(scope="session")
def test_data(db):

    correctness_tester = Seeder.SeedTestDatabase()

    return correctness_tester

# @pytest.fixture(scope='session')
# def _db():
#     return db


@pytest.fixture(scope='function')
def redis_clear(request: pytest.FixtureRequest):
    from Backend.Blueprints.Commands.command_result_queue import Command_Queue, Result_Dict
    command = Command_Queue()
    result = Result_Dict()

    def teardown():
        command.clear()
        result.clear()
    
    teardown()

    request.addfinalizer(teardown)

@pytest.fixture(scope='function')
def db_session(db: SQLAlchemy, request: pytest.FixtureRequest):
    """
    Creates a session which is scoped to this pytest
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, join_transaction_mode="create_savepoint")
    session = db._make_scoped_session(options=options)
    nested = connection.begin_nested()

    # old = db.session
    # db.session = session

    # def teardown():
    #     session.rollback()
    #     session.close()
    #     transaction.rollback()
    #     connection.close()

    #     db.session = old
    
    # request.addfinalizer(teardown)
    yield session

    transaction.rollback()
    session.close()
    connection.close()
    

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
def event(db_session: Session):
    
    event = Seeder.event_factory()

    assert not isinstance(event, list)
    return event

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
