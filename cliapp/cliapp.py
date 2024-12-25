#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
Simple CLI application, template for CLI module/package development
"""
import logging

from cliapp.cliparams import cli_argument_parser


def do_the_work(input_file, output_file):
    logging.info("Input file: %s", input_file)
    logging.info("Output file: %s", output_file)


def main():
    args = cli_argument_parser(None)

    do_the_work(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
