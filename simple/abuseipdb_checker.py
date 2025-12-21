import argparse
import ipaddress
import json
import logging
import os
import sys
from pprint import pformat

import httpx
from dotenv import load_dotenv

# Defining the api-endpoint
ABUSEIPDB_API_ENDPOINT = 'https://api.abuseipdb.com/api/v2/check'

def get_querystring(ip_address: str) -> dict:
    ip_obj = ipaddress.IPv4Address(ip_address)

    return {
        'ipAddress': str(ip_obj),
        'maxAgeInDays': '180'
    }

def get_headers() -> dict:
    return {
        'Accept': 'application/json',
        'Key': os.getenv('ABUSEIPDB_API_KEY', 'NO_KEY_PROVIDED')
    }


def logger_setup(cli_params: argparse.Namespace) -> None:
    logging.basicConfig(
        level=(logging.DEBUG if cli_params.verbose else logging.INFO))

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logging.debug("CLI arguments: %s", pformat(cli_params))


def args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('-o', '--output',
                        help='name of the output file',
                        required=True)

    parser.add_argument('-i', '--input',
                        help='name of the input file',
                        required=True)

    return parser.parse_args()


def main():
    params = args_parser()

    load_dotenv()

    logger_setup(params)

    with open(params.input, 'r', encoding='utf-8') as in_file:
        ip_addresses = in_file.read().splitlines()

    with open(params.output, 'w', encoding='utf-8') as out_file:
        for ip_address in ip_addresses:
            ip_address = ip_address.strip()

            try:
                response = httpx.get(url=ABUSEIPDB_API_ENDPOINT,
                                     headers=get_headers(),
                                     params=get_querystring(ip_address))
                response.raise_for_status()
                decoded_response = response.json()

                logging.debug("Received response for IP %s: %s", ip_address, pformat(decoded_response))

                ip_details = {
                    'ipAddress': decoded_response['data']['ipAddress'],
                    'abuseConfidenceScore': decoded_response['data']['abuseConfidenceScore'],
                    'countryCode': decoded_response['data']['countryCode'],
                    'usageType': decoded_response['data']['usageType'],
                    'isp': decoded_response['data']['isp']
                }

                json.dump(ip_details, out_file)
                out_file.write('\n')

            except httpx.HTTPError as e:
                logging.error("HTTP error occurred for IP %s: %s", ip_address, str(e))


if __name__ == "__main__":
    main()
