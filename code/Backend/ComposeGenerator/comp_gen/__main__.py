import argparse
import logging

from . import run
CHOICES=(
        "config",
        "locations"
    )
class Help(argparse.Action):

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: str | None, option_string: str | None = None) -> None:
        if values is None:
            raise RuntimeError("No value passed to help")
        
        match values:
            case "locations":
                from comp_gen.common import BasicConfig
                print("Valid Locations for Configuration: ")
                for i in BasicConfig.LOCATION_NETWORKS.keys():
                    print(f'\t{i}')
                exit()
            case 'config':
                from comp_gen.schema.config import ConfigElementSchema
                print(ConfigElementSchema.help())
                exit()
            case _:
                print("No help of that name:\n\nValid Help Fields: {}".format(CHOICES))
                exit()

            



def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate docker compose file for 90snet")

    parser.add_argument("config_path", type=argparse.FileType('r'), help="Input configuration file")
    parser.add_argument('output_path', type=argparse.FileType('w'), help="Output docker compose file")
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-t", "--topic", action=Help, help="Help about different config topics. Valid Help Fields: {}".format(CHOICES))

    return parser.parse_args()

def main():
    args = get_args()

    logging.basicConfig(
            format='┌─╴[{levelname:s}|{filename:s}|{funcName:s}-{lineno:d}]\n└╴{message:s}\n',
        level=logging.DEBUG if args.verbose else logging.INFO,
        style='{',
    )

    print("Running Now")
    run(args.config_path, args.output_path)


if __name__ == "__main__":
    main()
