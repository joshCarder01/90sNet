from marshmallow import Schema, fields, validate, post_load

from comp_gen.common import BasicConfig
from comp_gen.network import NETWORK

__COUNT_ERROR_STR="Count field must have atleast 1 as its value"

class ConfigElement:
    image: str
    count: int
    proxy: bool
    location: str

    def __init__(self, image: str, count: int, location: str, proxy: bool = False, other_options = None):
        self.image = image
        self.count = count
        self.location = location
        self.proxy = proxy
        self.other_options = other_options

class ConfigElementSchema(Schema):
    image = fields.Str(required=True)
    count = fields.Integer(
                load_default=1,
                validate=validate.Range(
                    min=1,
                    error="Count field must have atleast 1 as its value"
                )
                )
    proxy = fields.Bool(load_default=False)
    location = fields.Str(
        required=True,
        validate=validate.OneOf(
            BasicConfig.locations(),
            error="Invalid location in config"
        )
    )
    other_options = fields.Dict(
        required=False,
        allow_none=True
    )
