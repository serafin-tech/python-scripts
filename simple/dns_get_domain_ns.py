#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
Read NS records for domain
"""
import argparse
import json
import logging
import sys
from pprint import pformat

import dns.resolver
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

    parser.add_argument('domain',
                        type=str,
                        help='Domain name to get NS records')

    return parser.parse_args()


def logger_setup(cli_params: argparse.Namespace) -> None:
    logging.basicConfig(
        level=(logging.DEBUG if cli_params.verbose else logging.INFO))

    logging.debug("CLI arguments: %s", pformat(cli_params))


def main(domain: str) -> dict[str, str | list[str]]:
    logging.debug("Getting NS server details for domain: %s", domain)

    validators.domain(domain)

    dns_answers = dns.resolver.resolve(domain, 'NS')

    ns_fqdns = sorted({rdata.target.to_text(omit_final_dot=True) for rdata in dns_answers})

    logging.debug("DNS answers: %s", ns_fqdns)

    output_data = {
        'domain': domain,
        'nameservers': ns_fqdns
    }

    return output_data


if __name__ == "__main__":
    args = args_parser()

    logger_setup(args)

    json.dump(main(args.domain), sys.stdout, indent=None)
