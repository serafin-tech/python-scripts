#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
RDAP information retiver for domain details
"""
import argparse
import json
import logging
import sys
from pprint import pformat
from typing import Any

import httpx
import validators


def get_file_content(file_name) -> list[str]:
    with open(file_name, mode='r', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def args_parser() -> argparse.Namespace:
    """
    CLI argument parser
    :return: argparse.Namespace with parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('domain',
                        type=str,
                        help='Domain name to get RDAP details for')

    return parser.parse_args()


def logger_setup(cli_params: argparse.Namespace) -> None:
    logging.basicConfig(
        level=(logging.DEBUG if cli_params.verbose else logging.INFO))

    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.debug("CLI arguments: %s", pformat(cli_params))


def main(domain: str) -> dict[str, Any] | None:
    logging.debug("Getting RDAP details for domain: %s", domain)

    validators.domain(domain)

    rdap_data = httpx.get(
        f"https://rdap.org/domain/{domain}", follow_redirects=True)

    if rdap_data.status_code == 404:
        logging.info(
            "Authoritative RDAP source unknown for domain: %s", domain)
        return None

    rdap_data.raise_for_status()

    logging.debug("RDAP data received: %s", pformat(rdap_data.json()))

    nameservers = [item.get('ldhName')
                   for item in rdap_data.json().get('nameservers', [])]

    registar = [item.get('vcardArray')
                for item in rdap_data.json().get('entities', [])
                if 'registrar' in item.get('roles', [])]

    output_data = {
        'domain': domain,
        'nameservers': nameservers,
        'entities': registar
    }

    logging.debug("Details for %s\n%s", domain,
                  json.dumps(output_data, indent=None))

    return output_data


if __name__ == "__main__":
    args = args_parser()

    logger_setup(args)

    json.dump(main(args.domain), sys.stdout, indent=None)
