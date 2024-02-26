import datetime

from dataclasses import dataclass

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from .base import Serializer
from Backend import db

__all__ = ['ScoreEvent']

EPOCH= datetime.datetime.fromtimestamp(0, datetime.UTC)
@dataclass
class ScoreEvent(db.Model, Serializer):

    __tablename__ = "event"

    id: Mapped[int]         = mapped_column(Integer, primary_key=True)
    #name: Mapped[str]       = mapped_column(Text, nullable=False)
    time: Mapped[DateTime]  = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    user_id: Mapped[int]    = mapped_column(ForeignKey('user.id'))
    machine_id: Mapped[int] = mapped_column(ForeignKey('machine.id'))

    @property
    def timestamp(self):
        return datetime.datetime.timestamp(self.time)

    def serialize(self):
        data = Serializer.serialize(self)
        data["time"] = self.timestamp
        return data