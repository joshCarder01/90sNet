import yaml
import sys

from typing import List
from marshmallow import ValidationError

from .schema.config import ConfigElementSchema, ConfigElement
from .docker import ContainerSet


def read_config(input) -> ContainerSet:

    raw = yaml.load(input, yaml.SafeLoader)

    print(f"Raw: {raw}")
    # Deserialize the raw dictionary
    deserializer = ConfigElementSchema(many=True)

    config: List[dict] = deserializer.load(raw)

    intermediate = []
    for i in config:
        intermediate.append(ContainerSet(**i))

    main_set: ContainerSet = intermediate.pop(0)

    for i in intermediate:
        main_set.append(i)



    return main_set
