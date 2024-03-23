import json

from contextlib import AbstractContextManager
from types import TracebackType
from flask import request, current_app, has_request_context
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError

from Backend.exceptions import MissingJSONKey

class NamedTupleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            return obj._asdict()
        return json.JSONEncoder.default(self, obj)


class HandleJSON(AbstractContextManager):
    """
    Handles KeyErrors in flask. Intended to be used on JSON, will raise an error if there is no request context.
    """
    def __init__(self):
        if not has_request_context():
            raise RuntimeError("SafeJSONLoad cannot be used outside of request context")

    def __enter__(self):
        self.checkJSON()

        return
    
    def __exit__(
                    self,
                    __exc_type: type[BaseException] | None,
                    __exc_value: BaseException | None,
                    __traceback: TracebackType | None
                ) -> bool | None:

        if __exc_type is KeyError:
            _key = __exc_value.args[0]

            current_app.logger.exception("[%s]: Key Missing from JSON: %s",
                                                request.path, _key)
            
            current_app.logger.debug("Input json: %s", str(request.json))
            

            # Using the key error we will raise the new error to be handled by the applicaiton
            raise MissingJSONKey(_key) from __exc_value
    
    def checkJSON(self) -> None:

        if request.json is None:
            raise BadRequest("Request Requires JSON")
            
from sqlalchemy.orm import DeclarativeBase
class _DBBase(DeclarativeBase):
    def __str__(self):
        return f"{str(self.__tablename__)}: {(i for i in self.col_names)}"