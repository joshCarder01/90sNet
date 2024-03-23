from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

__all__=['_DBBase']

class _DBBase(DeclarativeBase):
    def __str__(self):
        return f"{str(self.__talbename__)}: {(i for i in self.col_names)}"


class Serializer(object):

    @property
    def col_names(self):
        return [k for k in inspect(self).attrs.keys()]

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
    
    def json_col_match(self, json_object: dict):
        return all((i in json_object.keys() for i in self.col_names))
    
    def json_comp(self, json_object: dict):
        return all((getattr(self, i) == json_object[i] for i in self.col_names))
