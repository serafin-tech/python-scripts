#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
"""
script to convert csv to Markdown table

required modules:
- beautifulsoup4~=4.13.5
- httpx~=0.28.1
- tabulate~=0.9
- validators~=0.35.0
"""

import argparse
import logging
import sys
from pprint import pformat
from typing import List

import httpx
import validators
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('profile_url',
                        help='url to CloudSkillBoost public profile')

    parser.add_argument('-o', '--output_file',
                        default='-',
                        help='Markdown file to be written, default stdout')

    return parser.parse_args()


def write_markdown_table(data: List[List[str]], output_file_name: str):
    if output_file_name == '-':
        output_file = sys.stdout
    else:
        # pylint: disable=consider-using-with
        output_file = open(output_file_name, 'w', encoding='utf-8')
    try:
        markdown_table = tabulate(data, headers="firstrow", tablefmt="github")
        output_file.write(markdown_table)
        output_file.write('\n')
    finally:
        if output_file is not sys.stdout:
            output_file.close()


def get_payload(profile_url: str) -> str:
    if validators.url(profile_url):
        response = httpx.get(profile_url)
        response.raise_for_status()
        return response.text

    raise ValueError(f"Invalid URL: {profile_url}")


def read_profile_data(profile_url: str) -> List[List[str]]:
    soup = BeautifulSoup(get_payload(profile_url), 'html.parser')
    parent_div = soup.find('div', class_='profile-badges')
    badge_divs = parent_div.find_all('div', class_='profile-badge')

    ret:List[List[str]] = [['Badge name', 'Date earned']]

    for badge in badge_divs:
        # <span class='ql-title-medium l-mts'>
        # Managing Security in Google Cloud
        # </span>
        # <span class='ql-body-medium l-mbs'>
        # Earned Sep 10, 2025 EDT
        # </span>
        badge_name = badge.find('span', class_='ql-title-medium l-mts').get_text(strip=True)
        badge_date = badge.find('span', class_='ql-body-medium l-mbs').get_text(strip=True).replace('Earned ', '')
        ret.append([badge_name, badge_date])

    return ret


def main():
    cli_arguments = get_cli_arguments()

    if cli_arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug("CLI arguments: %s", pformat(cli_arguments))

    payload = read_profile_data(cli_arguments.profile_url)
    logging.debug("Profile payload: %s", pformat(payload))

    write_markdown_table(payload, cli_arguments.output_file)


if __name__ == "__main__":
    main()
