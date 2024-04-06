from dataclasses import dataclass

from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Serializer

from Backend import db

__all__ = ['User']

@dataclass
class User(db.Model, Serializer):

    __tablename__ = "user"

    id: Mapped[int]                 = mapped_column(Integer, primary_key=True)
    username: Mapped[str]           = mapped_column(Text, nullable=False, unique=True)
    name: Mapped[str]               = mapped_column(Text, nullable=True)

    def __str__(self):
        return f"User({self.id}, {self.username}, {self.name})"
    