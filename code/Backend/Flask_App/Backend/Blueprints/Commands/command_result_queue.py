"""
"""
from flask import current_app, abort
from random import randint
from typing import Union, List, TypedDict
from collections.abc import Iterable
from abc import abstractmethod, ABC
from datetime import timedelta

import sys
from redis import Redis

from marshmallow import Schema, fields

def rand_id() -> int:
    return randint(0, sys.maxsize)

class TypedCommand(TypedDict):
    cmd: str
    args: str
    id: int

class CommandSchema(Schema):
    cmd = fields.Str(required=True)                     # A string
    args = fields.List(fields.Str(), required=True)     # Just a different string
    id = fields.Int(load_default=rand_id)               # Random Id

commandschema = CommandSchema()

class TypedResult(TypedDict):
    result: str
    id: int

class ResultSchema(Schema):
    result = fields.Str(required=True)
    id = fields.Int(required=True)

resultschema = ResultSchema()


class BaseConnector(ABC):
    
    @classmethod
    def __get_connection(cls):
        return Redis(
                        current_app.config["REDIS_DATABASE_HOST"],
                        current_app.config['REDIS_DATABASE_PORT'],
                        decode_responses=True
                    )

    def __init__(self):
        self._connection = Command_Queue.__get_connection()
    
    def __del__(self):
        if self._connection is not None:
            self._connection.close()
    
    def clear(self):
        self.connection.delete(self.key)

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Command_Queue.__get_connection()
        return self._connection
    
    @property
    @abstractmethod
    def key(self):
        return "Something"

class Command_Queue(BaseConnector):
    __key = "90snet:cmd_queue"

    @property
    def key(self):
        return self.__key
    
    def __len__(self):
        return self.connection.llen(self.key)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self) == 0:
            raise StopIteration()
        return self.deque()

    def enqueue(self, command: TypedCommand):
        return self.connection.rpush(self.key, commandschema.dumps(command))
    
    def deque(self) -> Union[TypedCommand, None]:
        if self.connection.llen(self.key) > 0:
            return commandschema.loads(self.connection.lpop(self.key))
        return None


class Result_Dict(BaseConnector):
    __key = "90snet:results:"

    @property
    def key(self):
        return self.__key
    
    @property
    def search_key(self):
        return self.__key + "*"
    
    def id_key(self, id: int):
        return self.__key + str(id)
    
    def __setitem(self, key: int, value: TypedResult):
        return self.set_result(value)
    
    def __getitem__(self, key: int) -> Union[TypedResult, None]:
        return self.get_result(key)
    
    def __len__(self):
        return len(self.connection.keys(self.search_key))
    
    def clear(self):
        removal = self.connection.keys(self.search_key)
        if len(removal) == 0:
            return
        return len(removal) == self.connection.delete(*removal)

    def set_result(self, data: TypedResult):
        self.connection.set(self.id_key(data["id"]), resultschema.dumps(data))
    
    def get_result(self, id: int) -> Union[TypedResult, None]:
        data = self.connection.get(self.id_key(id))
        if data is not None:
            # Set an expiration time for the result to prevent memeory leakage
            self.connection.expire(self.id_key(id), timedelta(minutes=2))
        return resultschema.loads(data)

def _panic(problematic):
    current_app.logger.error("Something caused the enqueing to fail!\n%s", str(problematic))
    abort(500)


def add_command(command_string: str, args: List[Union[str, int]]) -> int:
    """
    The assumption made here is that the process of adding the command to the 
    queue is synchronus, send a post request, then get a response with the id
    of the command submitted.
    """
    if not isinstance(command_string, str):
        raise TypeError(f"Command String is an invalid type: {type(command_string)} - {command_string}")

    id = rand_id()

    queue = Command_Queue()

    cmd_object: TypedCommand = commandschema.load({'cmd': command_string, 'args': args, 'id': id})
    if not queue.enqueue(cmd_object):
        _panic(cmd_object)

    return id

def pop_command() -> (str | None):
        queue = Command_Queue()

        return queue.deque()

def add_result(result: str, id: int) -> int:
    
    results = Result_Dict()

    rslt_obj = resultschema.load(dict(
        result=result,
        id=id
    ))
    if not results.set_result(rslt_obj):
        _panic(rslt_obj)

    return id


def get_result(id: int) -> Union[str, None]:
    results = Result_Dict()

    return results[id]
