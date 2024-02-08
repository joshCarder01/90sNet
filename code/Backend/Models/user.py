from dataclasses import dataclass
from typing import List

from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from .base import _DBBase
from .pwn_event import PwnEvent

__all__ = ['User']

@dataclass
class User(_DBBase):

    __tablename__ = "user"

    id: Mapped[int]                 = mapped_column(Integer, primary_key=True)
    username: Mapped[str]           = mapped_column(Text, nullable=False, unique=True)
    name                            = mapped_column(Text, nullable=True)
    #events: List[Mapped["Event"]]   = Relationship("Event", back_populates="user_id")
    