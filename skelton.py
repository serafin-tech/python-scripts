#!/usr/bin/env python3

"""
skelton script to speed-up development
"""

from pprint import pprint
import argparse
import csv
import json


def json2dict(fname: str):
    """
    function to serialize json into dictionary
    """
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return {}


def write_csv(fname: str, content: list):
    """
    function to write list of lists as CSV file
    """
    with open(fname, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)

        writer.writerows(content)


def args_parser():
    """
    argument parser, returns arguments as a tupple
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('infile',
                        help='file to be processed')
    parser.add_argument('outfile',
                        help='file to write output to')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    params = parser.parse_args()

    return params.infile, params.outfile


def main(inf: str, outf: str):
    """
    main function of the skelton
    """
    with open(inf, "r", encoding="utf-8") as file:
        for line in file:
            pprint(line)

    payload = [
        ['a1', 'b1', 'c1'],
        ['a2', 'b2', 'c2'],
        ['a3', 'b3', 'c3'],
    ]

    write_csv(outf, payload)


if __name__ == "__main__":
    infile, outfile = args_parser()

    main(infile, outfile)
