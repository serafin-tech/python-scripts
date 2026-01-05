#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
RDAP information retiever for domain details

required ubuntu packages:
    - python3-validators
    - python3-httpx
"""
import argparse
import json
import logging
import sys
import time
from pprint import pformat
from typing import Any

import httpx
import validators


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

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-d', '--domain',
                       type=str,
                       help='Domain name to get NS records')
    group.add_argument('-f', '--file',
                       type=str,
                       help='Path to file with domains (one per line)')

    return parser.parse_args()


def logger_setup(cli_params: argparse.Namespace) -> None:
    logging.basicConfig(
        level=(logging.DEBUG if cli_params.verbose else logging.INFO))

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logging.debug("CLI arguments: %s", pformat(cli_params))


def get_rdap_data(domain: str) -> dict[str, str | list[Any]]:
    logging.debug("Getting RDAP details for domain: %s", domain)

    validators.domain(domain)

    rdap_data = httpx.get(
        f"https://rdap.org/domain/{domain}", follow_redirects=True)
    time.sleep(1)

    if rdap_data.status_code == 404:
        logging.info(
            "Authoritative RDAP source unknown for domain: %s", domain)
        return {
            'domain': domain,
            'nameservers': None,
            'registar': None
        }

    if rdap_data.status_code == 403:
        logging.info(
            "RDAP access forbidden for domain: %s", domain)
        return {
            'domain': domain,
            'nameservers': None,
            'registar': None
        }


    rdap_data.raise_for_status()

    logging.debug("RDAP data received: %s", pformat(rdap_data.json()))

    nameservers = [item.get('ldhName')
                   for item in rdap_data.json().get('nameservers', [])]

    try:
        registar = [[inneritem for inneritem in item.get('vcardArray', [])[1] if inneritem[0] == 'fn'][0][3]
                    for item in rdap_data.json().get('entities', [])]
    except (IndexError, KeyError):
        registar = None

    output_data = {
        'domain': domain,
        'nameservers': nameservers,
        'registar': registar
    }

    logging.debug("Details for %s\n%s", domain,
                  json.dumps(output_data, indent=None))

    return output_data


def main(domains: list[str]) -> None:
    logging.debug("Getting RDAP details for domains: %s", pformat(domains))

    output_data = [get_rdap_data(item) for item in domains]

    json.dump(output_data, sys.stdout, indent=4, ensure_ascii=True)


if __name__ == "__main__":
    args = args_parser()

    logger_setup(args)

    domains: list[str] = []
    if args.domain:
        domains.append(args.domain)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as file:
            domains = [line.strip() for line in file.read().splitlines()
                       if line.strip() or line.strip().startswith('#') is False]

    main(domains)
