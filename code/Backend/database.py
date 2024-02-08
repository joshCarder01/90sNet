import datetime
import random
import logging

from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql import func

from typing import Union

from Models.base import _DBBase
from Models import PwnEvent, User, Machine

__all__=['DBManager']

MAX_INT=99999999

class DBManager:
    
    engine: Engine = None
    __model_base: _DBBase = _DBBase

    def __init__(self, path: str):
        self.create_db(path)

    def create_db(self, path: str):
        logging.info("Creating Database at: {}", path)
        self.engine = create_engine("sqlite:///" + path)
        self.__model_base.metadata.create_all(self.engine)


    def events_since(self, time_since: datetime.datetime):
        select(PwnEvent).where(PwnEvent.time >= time_since).order_by(PwnEvent.time)
    
    def __enter__(self):
        return Session(self.engine)

    def get_session(self, **kwargs):
        """
        Intended to act as a method to quickly gain a new session to work in.
        This is not meant to be one single session and each interaction
        should close its own session.
        """
        return Session(self.engine, **kwargs)


class Seeder:

    def __init__(self, Manager: DBManager):
        self.manager = Manager

    def __get_random_id(self, model: Union[User, Machine]):
        """
        Gets a random id from the selected table
        """

        with self.manager.get_session() as session:
            return session.query(model).options(load_only('id')).offset(
                func.floor(
                    func.random() *
                    session.query(func.count(model.id))
                    )
                ).limit(1).all()

    
    def user_factory(self, num_records: int=10, base_name: str="User_"):
        
        # Creating this number of records
        with Session(self.manager.engine) as session:
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

        with Session(self.manager.engine) as session:
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
        with Session(self.manager.engine) as session:
            for i in range(num_records):
                session.add(
                    PwnEvent(
                        id = random.randint(0, MAX_INT),
                        time = current - datetime.timedelta(seconds=random.randint(0, max_sec_past)),
                        user_id = self.__get_random_id(User),
                        machine_id = self.__get_random_id(Machine)
                    )
                )
            
            session.commit()

if __name__ == "__main__":
    manager = DBManager("db/testing.sqlite")

    seed = Seeder(manager)

    seed.user_factory(20)
    seed.machine_factory(10)
    seed.pwn_event_factory(30)

