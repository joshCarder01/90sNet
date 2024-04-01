import argparse
import logging

from . import run

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate docker compose file for 90snet")
    parser.add_argument("config_path", type=argparse.FileType('r'), help="Input configuration file")
    parser.add_argument('output_path', type=argparse.FileType('w'), help="Output docker compose file")
    parser.add_argument("-v", "--verbose", action='store_true')

    return parser.parse_args()

def command_run():
    args = get_args()

    logging.basicConfig(
        format='[%(levelname)s|%(filename)s|%(funcName)s-%(lineno)d]: %(message)s',
        level=logging.DEBUG if args.verbose else logging.INFO
    )


    print("Running Now")
    run(args.config_path, args.output_path)


if __name__ == "__main__":
    command_run()