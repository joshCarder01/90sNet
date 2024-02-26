import click
import datetime
import random
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql import func

from typing import Union

from Backend import db
from Backend.Models import ScoreEvent, User, Machine
from flask import (
    Blueprint
)

MAX_INT=99999999

class Seeder:

    def __get_random_id(self, model: Union[User, Machine]):
        """
        Gets a random id from the selected table
        """
        return db.session.query(model).order_by(func.random()).first().id

    
    def user_factory(self, num_records: int=10, base_name: str="User_"):
        
        # Creating this number of records
        with Session(db.engine) as session:
            for i in range(num_records):
                session.add(
                    User(
                        id=random.randint(0,MAX_INT),
                        username=base_name+str(i)
                    )
                )

            session.commit()
    
    def machine_factory(self, 
                            num_records: int=10,
                            machine_name: str = "machine_",
                            score_min: int = 100,
                            score_max: int = 1000,
                            score_step: int = 100
                        ):

        with Session(db.engine) as session:
            for i in range(num_records):
                session.add(
                    Machine(
                        id = random.randint(0,MAX_INT),
                        name = machine_name + str(i),
                        score = random.randrange(score_min, score_max, score_step)
                    )
                )

            session.commit()
    
    def pwn_event_factory(self,
                        num_records: int = 10,
                        max_sec_past: int = 600
                    ):
        
        current = datetime.datetime.now()
        with Session(db.engine) as session:
            for i in range(num_records):
                session.add(
                    ScoreEvent(
                        id = random.randint(0, MAX_INT),
                        type = "score_event",
                        time = current - datetime.timedelta(seconds=random.randint(0, max_sec_past)),
                        user_id = self.__get_random_id(User),
                        machine_id = self.__get_random_id(Machine)
                    )
                )
            
            session.commit()

database_cli = Blueprint("db", __name__)


@database_cli.cli.command("init")
def seed_database():

    db.drop_all()
    db.create_all()

    seed = Seeder()

    seed.user_factory(20)
    seed.machine_factory(10)
    seed.pwn_event_factory(30)

