from dataclasses import dataclass
from sqlalchemy import Integer, Text
from sqlalchemy.orm import mapped_column

from .base import _DBBase

__all__ = ['Machine']

@dataclass
class Machine(_DBBase):

    __tablename__ = "machine"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, nullable=False, unique=True)
    score = mapped_column(Integer, nullable=False)
