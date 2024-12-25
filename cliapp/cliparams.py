"""
Code for CLI argument parsing/processing
"""
import argparse
import logging
from typing import List

from ._version import __version__


def cli_argument_parser(argument_list: List[str] | None) -> argparse.Namespace:
    """
    argument parser, returns arguments as a tupple
    """
    parser = argparse.ArgumentParser(prog=f'cliapp version:{__version__}',)

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('input_file',
                        help='file to be processed')
    parser.add_argument('output_file',
                        help='file to write output to')

    cli_parameters = parser.parse_args(argument_list)

    logging.basicConfig(
        level=(logging.DEBUG if cli_parameters.verbose else logging.INFO))

    return cli_parameters
