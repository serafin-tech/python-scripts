#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
"""
reading multiple CSV files and combining them into a single Excel file
"""

import argparse
import csv
import logging

from openpyxl import Workbook # pylint: disable=import-error


def csv_reader(input_file_name: str) -> list:
    with open(input_file_name, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file)

        ret_list = []
        for row in reader:
            ret_list.append(row)

        return ret_list


def get_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('input_file',
                        nargs='+',
                        help='CSV files to be imported')

    parser.add_argument('output_file',
                        help='Excel file to be written')

    return parser.parse_args()


def main():
    cli_arguments = get_cli_arguments()

    if cli_arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    work_book = Workbook()
    work_book.remove(work_book.active)

    for input_file in cli_arguments.input_file:
        logging.info("Reading file: %s", input_file)

        csv_data = csv_reader(input_file)

        sheet = work_book.create_sheet(title=input_file)
        for row in csv_data:
            sheet.append(row)

    logging.info("Writing file: %s", cli_arguments.output_file)
    work_book.save(cli_arguments.output_file)


if __name__ == "__main__":
    main()
