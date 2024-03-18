from sqlalchemy.sql import func

from Backend import db
from Backend.Models.seeder import Seeder
from flask import (
    Blueprint
)

database_cli = Blueprint("db", __name__, cli_group='db')

def _init_db():
    db.drop_all()
    db.create_all()

@database_cli.cli.command("init")
def init_database():
    _init_db()


@database_cli.cli.command("random")
def random_seeder():
    _init_db()

    Seeder.user_factory(20)
    Seeder.machine_factory(10)
    Seeder.pwn_event_factory(30)

@database_cli.cli.command("seed")
def test_seeder():
    _init_db()

    Seeder.SeedTestDatabase()

