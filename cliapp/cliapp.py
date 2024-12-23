#!/usr/bin/env python3
from cliapp.cliparams import cli_argument_parser


def do_the_work(input_file, output_file):
    pass


def main():
    args = cli_argument_parser(None)

    do_the_work(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
