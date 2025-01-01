#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
Script for generating a JSON file with Google API IP addresses.
"""
import argparse
import ipaddress
import json

from urllib.request import urlopen
from urllib.error import HTTPError


IPRANGE_URLS = {
    "goog": "https://www.gstatic.com/ipranges/goog.json",
    "cloud": "https://www.gstatic.com/ipranges/cloud.json",
}

DNS = ["8.8.4.0/24", "8.8.8.0/24"]

# source: https://cloud.google.com/vpc/docs/configure-private-google-access#config-options
EXTRA_CIDRS = ["34.126.0.0/18", "199.36.153.8/30", "199.36.153.4/30"]


def read_json_from_url(url: str) -> dict:
    try:
        return json.loads(urlopen(url).read())
    except (IOError, HTTPError) as exc:
        raise ValueError(f"Invalid HTTP response from {url}") from exc
    except json.decoder.JSONDecodeError as exc:
        raise ValueError(f"Could not parse HTTP response from {url}") from exc


def get_google_ipv4_prefixes(url: str):
    data = read_json_from_url(url)

    return [entry.get("ipv4Prefix")
           for entry in data["prefixes"] if "ipv4Prefix" in entry]


def get_out_file_from_args() -> str:
    parser = argparse.ArgumentParser()

    parser.add_argument('out_file',
                        help='name of the JSON output file')

    parsed_args = parser.parse_args()

    return parsed_args.out_file


def main():
    cidrs_ipv4 = {
        group: get_google_ipv4_prefixes(src_url)
        for group, src_url in IPRANGE_URLS.items()
    }

    google_api_addresses = set(cidrs_ipv4["goog"])
    google_api_addresses = google_api_addresses.difference(cidrs_ipv4["cloud"])
    google_api_addresses = google_api_addresses.difference(DNS)
    google_api_addresses.update(EXTRA_CIDRS)

    output_payload = sorted(list(google_api_addresses),
                            key=lambda x: ipaddress.IPv4Network(x).network_address.packed)

    with open(get_out_file_from_args(), 'w', encoding='utf-8') as out_file:
        out_file.write(json.dumps(output_payload, indent=4))


if __name__ == "__main__":
    main()
