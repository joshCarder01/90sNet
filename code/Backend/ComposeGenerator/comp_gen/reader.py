import yaml
import sys
import logging

from typing import List
from marshmallow import ValidationError

from .schema.config import ConfigElementSchema, ConfigElement
from .docker import ContainerSet


def read_config(input) -> ContainerSet:

    raw = yaml.load(input, yaml.SafeLoader)

    logging.debug("Raw: %s", str(raw))
    # Deserialize the raw dictionary
    deserializer = ConfigElementSchema(many=True)

    config: List[dict] = deserializer.load(raw)
    logging.debug("Deserialized: %s", str(config))

    intermediate = ContainerSet()
    for i in config:
        logging.debug("setup intermediate: %s", str(i))
        intermediate.append(**i)

    # logging.debug('Setup containersets from config output')

    # logging.debug('condensing containersets')
    # main_set: ContainerSet = intermediate.pop(0)

    # logging.debug('main_set: %s', main_set)
    # for i in intermediate:
    #     main_set.append(i)
    
    # logging.debug("Finished condensing containersets")

    logging.info("Configuration File Successfully Processed")

    return intermediate
