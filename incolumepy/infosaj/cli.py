import argparse
from pathlib import Path

import toml

from incolumepy.infosaj.infosaj import gen_infosaj

# Create the parser
my_parser = argparse.ArgumentParser(
    prog='infosaj',
    allow_abbrev=False,
    add_help=True,
    usage='%(prog)s [-h|-i|-m]',
    description='Informativo SAJ generator',
    epilog='Enjoy the program! :)',
)

print(Path(__file__).parents[2].joinpath("pyproject.toml"))
print(
    toml.load(
        Path(__file__).parents[2].joinpath("pyproject.toml")
    )['tool']['poetry']['version'])

my_parser.version = toml.load(
    Path(__file__).parents[2].joinpath("pyproject.toml")
)['tool']['poetry']['version']

my_parser.add_argument('-m',
                       '--model',
                       required=False,
                       # action='store',
                       action='store_true',
                       help='generate model.yaml file')

my_parser.add_argument('-i',
                       '--infosaj',
                       required=False,
                       # action='store',
                       action='store_true',
                       help='generate infosaj.html file')
