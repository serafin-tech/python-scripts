#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
skelton script to speed-up development
"""
from collections import namedtuple
from pprint import pprint
import argparse
import csv
import json
from typing import Dict, List

CLI_PARAMS = [
    {
        'name': 'input_file',
        'help': 'file to be processed'
    },
    {
        'name': 'output_file',
        'help': 'file to write output to'
    }
]

CliParams = namedtuple('CliParams', [item['name'] for item in CLI_PARAMS])


def get_file_content(file_name):
    with open(file_name, mode='r', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def json2dict(file_name: str) -> Dict:
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except IOError as err:
        print(err)
        return {'error': 'file operation error'}
    except json.JSONDecodeError as err:
        print(err)
        return {'error': 'JSON parsing error'}


def write_csv(file_name: str, content: list):
    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(content)


def args_parser(parameters_spec: List[Dict]) -> CliParams:
    """
    CLI argument parser
    :param parameters_spec: - list of dictionaries with 'name' and 'help' keys to define parser
    :return: CliParams named tuple with parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    for i in parameters_spec:
        parser.add_argument(i['name'], help=i['help'])

    parsed_args = parser.parse_args()

    ret_list = []
    for param in CliParams._fields:
        ret_list.append(getattr(parsed_args, param))

    return CliParams(*ret_list)


def main(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            pprint(line)

    payload = [
        ['a1', 'b1', 'c1'],
        ['a2', 'b2', 'c2'],
        ['a3', 'b3', 'c3'],
    ]

    write_csv(output_file, payload)


if __name__ == "__main__":
    args = args_parser(CLI_PARAMS)

    main(args.input_file, args.output_file)
