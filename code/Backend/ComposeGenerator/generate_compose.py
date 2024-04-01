import argparse
from comp_gen import run

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate docker compose file for 90snet")
    parser.add_argument("config_path", type=argparse.FileType('r'), required=True, help="Input configuration file")
    parser.add_argument('output_path', type=argparse.FileType('w'), required=True, help="Output docker compose file")

    return parser.parse_args()

def command_run(config_path, output_path):
    args = get_args()

    print("Running Now")
    run(args['config_path'], args['output_path'])


