from dataclasses import dataclass
from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Serializer, _DBBase

from Backend import db

__all__ = ['Machine']

@dataclass
class Machine(db.Model(model_class=_DBBase), Serializer):

    __tablename__ = "machine"

    id: Mapped[int]                 = mapped_column(Integer, primary_key=True)
    name: Mapped[str]               = mapped_column(Text, nullable=False, unique=True)
    location: Mapped[str]           = mapped_column(Text, nullable=False)
