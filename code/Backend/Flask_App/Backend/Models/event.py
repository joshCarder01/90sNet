import datetime

from dataclasses import dataclass
from enum import Enum as PyEnum
from typing import Any

from sqlalchemy import Integer, ForeignKey, DateTime, Text, types, Enum
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import mapped_column, Mapped

from .base import Serializer
from Backend import db

__all__ = ['Event']

EPOCH= datetime.datetime.fromtimestamp(0, datetime.UTC)
class EventTypesEnum(PyEnum):
    score = 0
    access = 1
    file_mod = 2
    root_dir_mod = 3
    cmd_changed_output = 4

    @classmethod
    def from_num(cls, id: int) -> str:
        return cls(id).name

# class EventType(types.TypeDecorator):
#     impl = types.Integer

#     def process_bind_param(self, value: str | int, dialect: Dialect) -> int:
#         # Fairly simple case since the input was a number which was in the enum
#         if value in EventTypesEnum:
#             return int(value)
#         else:
#             # May raise a KeyError
#             return EventTypesEnum[value]
    
#     # Should never be null, thus let an exception be raised if there is a problem
#     def process_result_value(self, value: int, dialect: Dialect) -> EventTypesEnum:
#         return EventTypesEnum(value)

@dataclass
class Event(db.Model, Serializer):

    __tablename__ = "event"

    id: Mapped[int]                     = mapped_column(Integer, primary_key=True)
    type: Mapped[EventTypesEnum]        = mapped_column(Enum(EventTypesEnum), nullable=False)
    time: Mapped[DateTime]              = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    user_id: Mapped[int]                = mapped_column(ForeignKey('user.id'), nullable=True)
    machine_id: Mapped[int]             = mapped_column(ForeignKey('machine.id'))

    @property
    def timestamp(self):
        return datetime.datetime.timestamp(self.time)

    def serialize(self):
        data = Serializer.serialize(self)
        data["time"] = self.timestamp
        data['type'] = self.type.name
        return data
    
    def json_comp(self, json_object: dict):

        return (
            json_object.get('id', None) == self.id and
            json_object.get('type', None) == self.type and
            json_object.get('time', None) == self.time and
            json_object.get('user_id', None) == self.user_id and
            json_object.get('machine_id', None) == self.machine_id
        )