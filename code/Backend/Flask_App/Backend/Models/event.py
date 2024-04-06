import datetime

from dataclasses import dataclass
from enum import Enum as PyEnum
from typing import Any

from sqlalchemy import Dialect, Integer, ForeignKey, DateTime, Enum, String, types
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Serializer
from .machine import Machine
from Backend import db

__all__ = ['Event']

EPOCH= datetime.datetime.fromtimestamp(0, datetime.UTC)
class EventTypesEnum(PyEnum):
    score = 0
    access = 1
    file_mod = 2
    root_dir_mod = 3
    cmd_changed_output = 4

    def __str__(self):
        return self.name

    @classmethod
    def from_num(cls, id: int) -> str:
        return cls(id).name
    
    @classmethod
    def get_names(cls):
        return [i.name for i in cls]

class EventType(types.TypeDecorator):
    impl = types.Integer

    def process_bind_param(self, value: str | int, dialect: Dialect) -> int:
        """
            This converts data on the way into the database
        """
        # Fairly simple case since the input was a number which was in the enum
        if isinstance(value, EventTypesEnum):
            return value.value
        elif isinstance(value, int):
            if value in EventTypesEnum:
                return value
        elif isinstance(value, str):
            return EventTypesEnum[value].value
        else:
            # May raise a KeyError
            return EventTypesEnum[value].value
    
    # Should never be null, thus let an exception be raised if there is a problem
    def process_result_value(self, value: int, dialect: Dialect) -> EventTypesEnum:
        return EventTypesEnum(value).name


def _default_time():
    return datetime.datetime.now(datetime.UTC)

@dataclass
class Event(db.Model, Serializer):

    __tablename__ = "event"

    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    type: Mapped[str]                   = mapped_column(EventType, nullable=False)
    time: Mapped[DateTime]              = mapped_column(DateTime, default=_default_time, nullable=False)
    user_id: Mapped[int]                = mapped_column(ForeignKey('user.id'), nullable=True)
    machine_id: Mapped[int]             = mapped_column(ForeignKey('machine.id'))
    machine_name: Mapped[str]           = mapped_column(String, nullable=False)
    description: Mapped[str]            = mapped_column(String, nullable=True)

    @property
    def timestamp(self):
        return datetime.datetime.timestamp(self.time)

    def serialize(self):
        data = Serializer.serialize(self)
        data["time"] = self.timestamp
        return data
            
    def json_comp(self, json_object: dict):

        return (
            json_object.get('id', None) == self.id and
            json_object.get('type', None) == self.type and
            json_object.get('time', None) == self.timestamp and
            json_object.get('user_id', None) == self.user_id and
            json_object.get('machine_id', None) == self.machine_id and
            json_object.get('description', None) == self.description
        )