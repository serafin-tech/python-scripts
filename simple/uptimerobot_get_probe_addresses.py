#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
get and process UptimeRobot probe addresses to import them to router.
"""
import argparse
import ipaddress

from string import Template
from urllib.request import urlopen, Request
from urllib.error import HTTPError


UPTIMEROBOT_CHECK_LOCATIONS = {
    "IPV4": "https://uptimerobot.com/inc/files/ips/IPv4.txt",
    "ALL": "https://uptimerobot.com/inc/files/ips/IPv4andIPv6.txt"
}

def read_addresses(location: str) -> list:
    try:
        if location not in UPTIMEROBOT_CHECK_LOCATIONS:
            raise ValueError(f"Invalid location: {location}")
        with urlopen(Request(url=UPTIMEROBOT_CHECK_LOCATIONS[location],
                             data=None,
                             headers={
                                'User-Agent': 'uptimerobot-probe-addresses-getter'
                             })) as response:
            return response.read().decode('utf-8').splitlines()
    except (IOError, HTTPError) as error:
        raise ValueError(f"Invalid HTTP response from {UPTIMEROBOT_CHECK_LOCATIONS[location]}") from error


def get_out_file_from_args() -> (str, str, str):
    parser = argparse.ArgumentParser()

    parser.add_argument('out_file',
                        help='name of the output file')

    parser.add_argument('--format',
                        help='output format',
                        choices=['mikrotik', 'fortigate', 'plain'],
                        default='plain')

    parser.add_argument('--addr-list-name',
                        help='address list name for Mikrotik or Fortigate output format',
                        default='UptimeRobot')

    parsed_args = parser.parse_args()

    return parsed_args.out_file, parsed_args.format, parsed_args.addr_list_name


def write_plain_list(output_payload, file_name):
    with open(file_name, 'w', encoding='utf-8') as out_file:
        for item in output_payload:
            out_file.write(f"{item}\n")


def write_mikrotik_list(output_payload, file_name, addr_list_name):
    initial_part_template = Template("/ip firewall address-list\n"
                                     "remove [find where list=${addr_list_name}]\n")
    initial_part = initial_part_template.substitute(addr_list_name=addr_list_name)

    line_template = Template("add address=${address} list=${addr_list_name}\n")

    with open(file_name, 'w', encoding='utf-8') as out_file:
        out_file.write(initial_part)
        for item in output_payload:
            out_file.write(line_template.substitute(
                address=item,
                addr_list_name=addr_list_name))


def main():
    out_file_name, out_format, out_addr_list_name = get_out_file_from_args()

    addresses = read_addresses("IPV4")

    output_payload = sorted(addresses,
                            key=lambda x: ipaddress.IPv4Network(x).network_address.packed)

    if out_format == 'mikrotik':
        write_mikrotik_list(output_payload, out_file_name, out_addr_list_name)
    elif out_format == 'fortigate':
        pass
    else:
        write_plain_list(output_payload, out_file_name)


if __name__ == "__main__":
    main()
