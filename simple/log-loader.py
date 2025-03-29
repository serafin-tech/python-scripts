#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
This script provides functionality to forward log entries from a specified log file
to a syslog server.

Usage:
    python log-loader.py [-d <syslog server ip>:<port>] <log_file>
"""
import argparse
import logging
import logging.handlers
import socket
from typing import List

from tqdm import tqdm

SYSLOG_SERVER = ('127.0.0.1', 2514)

def forward_log_entries(log_file_path: str, logger: logging.Logger) -> None:
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            for line in tqdm(log_file):
                logger.info(line.strip())
    except FileNotFoundError:
        print(f"File {log_file_path} not found.")

def cli_argument_parser(argument_list: List[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--destination',
                        default=':'.join(str(i) for i in SYSLOG_SERVER),
                        help='destination for the logs in format <syslog server ip>:<port>')

    parser.add_argument('-p',
                        '--protocol',
                        default='udp',
                        choices=['udp', 'tcp'],
                        help='syslog connection type, udp or tcp')

    parser.add_argument('log_file',
                        help='log file to load')

    cli_parameters = parser.parse_args(argument_list)

    return cli_parameters

def logger_config(syslog_server: str, syslog_port: int, syslog_protocol: str) -> logging.Logger:
    logger = logging.getLogger('log_forwarder')
    logger.setLevel(logging.INFO)

    syslog_handler = logging.handlers.SysLogHandler(
        address=(syslog_server, syslog_port),
        socktype=socket.SOCK_STREAM if syslog_protocol=='tcp' else socket.SOCK_DGRAM
    )

    formatter = logging.Formatter('%(message)s\n')
    syslog_handler.setFormatter(formatter)

    logger.addHandler(syslog_handler)

    return logger

if __name__ == "__main__":
    params = cli_argument_parser(None)
    dest_syslog_server, dest_syslog_port = params.destination.split(':')

    print(f"Loading logs from {params.log_file} to syslog server "
          f"at {dest_syslog_server}:{int(dest_syslog_port)} using {params.protocol} protocol...")

    forward_log_entries(params.log_file,
                        logger_config(dest_syslog_server, int(dest_syslog_port), params.protocol))
