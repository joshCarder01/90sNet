from dataclasses import dataclass
from typing import List

from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from .base import Serializer
from .score_event import ScoreEvent

from Backend import db

__all__ = ['User']

@dataclass
class User(db.Model, Serializer):

    __tablename__ = "user"

    id: Mapped[int]                 = mapped_column(Integer, primary_key=True)
    username: Mapped[str]           = mapped_column(Text, nullable=False, unique=True)
    name: Mapped[str]               = mapped_column(Text, nullable=True)
    #events: List[Mapped["Event"]]   = Relationship("Event", back_populates="user_id")
    