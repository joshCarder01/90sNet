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
    name = fields.Str(load_default=None)
    count = fields.Integer(
                allow_none=False,
                load_default=1,
                validate=validate.Range(
                    min=1,
                    error="Count field must have atleast 1 as its value"
                )
                )
    proxy = fields.Bool(load_default=False)
    locations = fields.List(
        fields.Str(
            validate=validate.OneOf(
                BasicConfig.locations(),
                error="Invalid location in config"
            ),
            required=True
        ),
        required=True,
    )
    other_options = fields.Dict(
        required=False,
        allow_none=True
    )

    def help():
        assemble = "Fields of the config:\n"
        assemble += "\tNAME\t\tTYPE\tREQ\tDESCRIPTION\n"
        assemble += "\timage\t\tstr\tT\tDocker Image to Run Container\n"
        assemble += "\tcount\t\tint\tT\tNumber of containers to run\n"
        assemble += "\tlocations\tstr\tT\tLocations to be used, list of the allowed locations\n"
        assemble += "\tproxy\t\tbool\tF\tIs this a proxy to be exposed to the outer world\n"
        assemble += "\tother_options\tdict\tF\tOther Docker Compose options to add at the end\n"
        return assemble
