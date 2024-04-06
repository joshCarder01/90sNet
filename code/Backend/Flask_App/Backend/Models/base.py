from sqlalchemy.inspection import inspect


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
