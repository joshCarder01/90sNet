"""
"""
from queue import Queue
from random import randint
from typing import NamedTuple, Union, List

import sys


class CmdStruct(NamedTuple):
    name: str
    args: List[Union[str, int]]
    id: int

    def serialize(self):
        return self._asdict()


class ResultStruct(NamedTuple):
    result: str
    id: int

    def serialize(self):
        return self._asdict()


# Should always init the command queue
net_command_queue: Queue[dict] = Queue() # type: ignore
net_command_results: Queue[dict] = Queue() # type: ignore

def rand_id() -> int:
    return randint(0, sys.maxsize)

def add_command(command_string: str, args: List[Union[str, int]]) -> int:
    """
    The assumption made here is that the process of adding the command to the 
    queue is synchronus, send a post request, then get a response with the id
    of the command submitted.
    """
    if not isinstance(command_string, str):
        raise TypeError(f"Command String is an invalid type: {type(command_string)} - {command_string}")

    id = rand_id()
    net_command_queue.put_nowait({
        "cmd": command_string,
        "args": args,
        "id": id
    })
    return id

def pop_command() -> (dict | None):
    if net_command_queue.empty():
        return None
    else:
        return net_command_queue.get_nowait()

def add_result(response: str, id: int) -> None:
    
    # Indicate a task was completed, idk why I would care but sure
    net_command_queue.task_done()

    net_command_results.put_nowait(dict(
        result=response,
        id=id
    ))
    return id


def get_all_results() -> List[dict]:
    output = []
    while not net_command_results.empty():
        output.append(net_command_results.get_nowait())
    net_command_results.unfinished_tasks = 0
    return output
