
from Backend import db
from Backend.Models import *

from datetime import datetime, UTC, timedelta
import random

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from typing import Union, Tuple, Dict

from Backend import db
from Backend.Models import Event, User, Machine

MAX_INT=99999999

class Seeder:

    seed_base_time = datetime(2024, 1, 1, 12, 0, 0, 0, UTC)
    seed_event_times = (
        seed_base_time,
        seed_base_time+timedelta(minutes=1, seconds=5),
        seed_base_time+timedelta(minutes=2, seconds=3),
        seed_base_time+timedelta(hours=1)
    )

    @classmethod
    def SeedTestDatabase(cls):
        db.drop_all()
        # Create the initial Database
        db.create_all()

        # Setting up some test users
        users = (
            User(id=453, username="testuser0",  name="User Name 0"),
            User(id=454, username="testuser1"),
            User(id=455, username="testuser2",  name="User Name 2")
        )

        db.session.add_all(users)

        # Setting up test machines
        machines = (
            Machine(id=1001, name="machine0", score=500),
            Machine(id=1002, name="machine1", score=800),
            Machine(id=1003, name="machine2", score=1000)
        )

        db.session.add_all(machines)


        # Setting up score events
        events = (
            Event(id=201, type="score", time=cls.seed_event_times[0], user_id=users[0].id, machine_id=machines[0].id),
            Event(id=202, type="score", time=cls.seed_event_times[1], user_id=users[0].id, machine_id=machines[1].id),
            Event(id=203, type="score", time=cls.seed_event_times[2], user_id=users[1].id, machine_id=machines[1].id),
            Event(id=204, type="score", time=cls.seed_event_times[3], user_id=users[2].id, machine_id=machines[2].id)
        )

        db.session.add_all(events)

        import uuid
        # Set up the runners
        # runners = (
        #     API_Runner("test1", uuid.UUID("3a96b22d-a241-4549-9bf9-82d3edf72ac6")),
        # )

        # db.session.add_all(runners)

        # Commit the database
        db.session.commit()

        # Object given to the test which contains all the correct values of the database
        correctness_tester: Dict[str, Union[Tuple[User], Tuple[Machine], Tuple[Event]]] = {
            "users": users,
            "machines": machines,
            "events": events,
            "runners": runners
        }

        return correctness_tester
    
    @classmethod
    def __get_random_id(cls, model: Union[User, Machine]):
        """
        Gets a random id from the selected table
        """
        return db.session.query(model).order_by(func.random()).first().id

    @classmethod
    def user_factory(cls, num_records: int=10, base_name: str="User_"):
        
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
    
    @classmethod
    def machine_factory(cls, 
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
    
    @classmethod
    def pwn_event_factory(cls,
                        num_records: int = 10,
                        max_sec_past: int = 600
                    ):
        
        current = datetime.now()
        with Session(db.engine) as session:
            for _ in range(num_records):
                session.add(
                    Event(
                        id = random.randint(0, MAX_INT),
                        type = random.choice(('score', 'access')),
                        time = current - timedelta(seconds=random.randint(0, max_sec_past)),
                        user_id = cls.__get_random_id(User),
                        machine_id = cls.__get_random_id(Machine)
                    )
                )
            
            session.commit()
