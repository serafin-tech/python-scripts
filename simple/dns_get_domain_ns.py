#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
Read NS records for domain

required ubuntu packages:
    - python3-dnspython
    - python3-validators
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

    logging.debug("CLI arguments: %s", pformat(cli_params))


def get_domain_nameservers(domain: str) -> dict[str, str | list[str] | None]:
    validators.domain(domain)

    try:
        dns_answers = dns.resolver.resolve(domain, 'NS')
    except (dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.resolver.NoAnswer) as err:
        logging.error("Domain does not exist: %s", domain)

        if isinstance(err, dns.resolver.NoAnswer):
            error_message = "No NS records found for domain"
        elif isinstance(err, dns.resolver.NoNameservers):
            error_message = "No nameservers available for domain"
        elif isinstance(err, dns.resolver.NXDOMAIN):
            error_message = "Domain does not exist"
        else:
            error_message = f"DNS error for domain {str(err)}"

        return {
            'domain': domain,
            'nameservers': error_message
        }

    ns_fqdns = sorted({rdata.target.to_text(omit_final_dot=True) for rdata in dns_answers})

    logging.debug("DNS answers: %s", ns_fqdns)

    return {
        'domain': domain,
        'nameservers': str(ns_fqdns)
    }


def main(domains2check: list[str]) -> None:
    logging.debug("Getting NS server details for domains: %s", pformat(domains2check))

    output_data = [get_domain_nameservers(item) for item in domains2check]

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
