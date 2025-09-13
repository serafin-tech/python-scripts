#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
"""
script to convert csv to Markdown table
"""

import argparse
import csv
import logging
import sys
from pprint import pformat
from typing import List

from tabulate import tabulate


def csv_reader(input_file_name: str) -> List[List[str]]:
    if input_file_name == '-':
        csv_file = sys.stdin
    else:
        # pylint: disable=consider-using-with
        csv_file = open(input_file_name, 'r', encoding='utf-8', newline='')
    try:
        reader = csv.reader(csv_file)
        return list(reader)
    finally:
        if csv_file is not sys.stdin:
            csv_file.close()


def write_markdown_table(data: List[List[str]], output_file_name: str):
    if output_file_name == '-':
        output_file = sys.stdout
    else:
        # pylint: disable=consider-using-with
        output_file = open(output_file_name, 'w', encoding='utf-8')
    try:
        markdown_table = tabulate(data, headers="firstrow", tablefmt="github")
        output_file.write(markdown_table)
        output_file.write('\n')
    finally:
        if output_file is not sys.stdout:
            output_file.close()


def get_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('-i', '--input_file',
                        default='-',
                        help='CSV files to be read, default stdin')

    parser.add_argument('-o', '--output_file',
                        default='-',
                        help='Markdown file to be written, default stdout')

    return parser.parse_args()


def main():
    cli_arguments = get_cli_arguments()

    if cli_arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug("CLI arguments: %s", pformat(cli_arguments))

    payload = csv_reader(cli_arguments.input_file)
    logging.debug("CSV payload: %s", pformat(payload))

    write_markdown_table(payload, cli_arguments.output_file)

if __name__ == "__main__":
    main()
