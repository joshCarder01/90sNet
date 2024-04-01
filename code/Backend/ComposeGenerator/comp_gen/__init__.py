import os
import yaml


from .reader import read_config
from .network import NETWORK
from .common import BasicConfig

def setup_dictionary(config_file):
    assembling = NETWORK

    # if not os.path.exists(config_path):
    #     raise FileNotFoundError("Config file not found!")
    
    # with open(config_path, 'r') as ifile:
    config = read_config(config_file)

    assembling[BasicConfig.SERVICES] = config.raw_dictionary()

    return assembling

def output_yaml(output_file, output_dict: dict): 

    # with open(output_file, 'w') as ofile:
    yaml.dump(output_dict, output_file, yaml.SafeDumper)


def run(input_path: str, output_path: str):
    data = setup_dictionary(input_path)

    output_yaml(output_file=output_path, output_dict=data)
