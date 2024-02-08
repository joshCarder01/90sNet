import datetime

from dataclasses import dataclass

from sqlalchemy import Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from .base import _DBBase

__all__ = ['PwnEvent']

@dataclass
class PwnEvent(_DBBase):

    __tablename__ = "event"

    id: Mapped[int]         = mapped_column(Integer, primary_key=True)
    #name: Mapped[str]       = mapped_column(Text, nullable=False)
    time: Mapped[DateTime]  = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)
    user_id: Mapped[int]    = mapped_column(ForeignKey('user.id'))
    machine_id: Mapped[int] = mapped_column(ForeignKey('machine.id'))
