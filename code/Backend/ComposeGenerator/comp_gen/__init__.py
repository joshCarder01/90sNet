import os
import yaml
import logging


from .reader import read_config
from .network import NETWORK
from .common import BasicConfig
version=0.1

def setup_dictionary(config_file):
    logging.info("Inputing configuration file")
    # if not os.path.exists(config_path):
    #     raise FileNotFoundError("Config file not found!")
    
    # with open(config_path, 'r') as ifile:
    config = read_config(config_file)

    logging.debug("config: %s", config)

    assembled = {
        BasicConfig.SERVICES: config.raw_dictionary(),
        **NETWORK
    }

    logging.debug(f"Assembled: {str(assembled)}")
    logging.info("Assembled Docker Compose Services into Dictionary")

    return assembled

def output_yaml(output_file, output_dict: dict): 

    logging.info("Outputting Compose YAML")
    # with open(output_file, 'w') as ofile:
    yaml.dump(output_dict, output_file, yaml.SafeDumper, sort_keys=False)


def run(input_path: str, output_path: str):
    data = setup_dictionary(input_path)

    output_yaml(output_file=output_path, output_dict=data)
