#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
"""
## ruamel.yaml Types

### 'safe'

Purpose: Security-focused parsing
Behavior: Only loads basic YAML types (strings, numbers, lists, dicts)
Limitations: Discards comments, formatting, and custom types
Use case: When processing untrusted YAML input where security is paramount

### 'rt' (Round-Trip)
Purpose: Preserves document structure and formatting
Behavior: Maintains comments, whitespace, quote styles, and anchor references
Returns: CommentedMap and CommentedSeq objects instead of plain dicts/lists
Use case: When you need to read, modify, and write YAML while preserving human-readable formatting

### 'unsafe'

Purpose: Full YAML 1.1 specification support
Behavior: Can load arbitrary Python objects (!!python tags)
Security: Dangerous - can execute arbitrary code
Use case: Only for trusted internal data where you need to serialize Python objects

### 'base'

Purpose: Minimal YAML processing
Behavior: Basic loading without extra features
Use case: When you need low-level control over YAML processing

### 'rtsc' (Round-Trip Safe Constructor)

Purpose: Round-trip mode with safe constructor
Behavior: Like 'rt' but only loads safe types
Use case: Preserving formatting while maintaining security constraints

Recommendation
For your use case (preserving comments and formatting from linter-compliant YAML):

```
yaml = YAML(typ='rt')  # Round-trip mode preserves everything
yaml.preserve_quotes = True
yaml.explicit_start = True  # Preserves ---
```

This gives you full formatting preservation while still being safe for general use.
"""
import argparse
import logging
import sys
from pprint import pformat

from ruamel.yaml import YAML


def args_parser(local_args: list[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('-i','--input_file',
                        type=str,
                        required=True,
                        help='input file to be processed')

    parser.add_argument('-o','--output_file',
                        type=str,
                        required=False,
                        default='',
                        help='output file to write results to')

    parsed_args = parser.parse_args(local_args)

    logging.basicConfig(
        level=(logging.DEBUG if parsed_args.verbose else logging.INFO))

    return parsed_args


def read_yaml_file(file_path: str) -> dict:
    yaml = YAML(typ='rt', pure=True)
    yaml.default_flow_style = False
    yaml.preserve_quotes = True

    with open(file_path, 'r', encoding='utf-8') as file:
        content = yaml.load(file)

    return content


def write_yaml_file(file_path: str, content: dict) -> None:
    yaml = YAML(typ='rt')
    yaml.default_flow_style = False
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=2, offset=2)
    yaml.explicit_start = True

    if not file_path:
        yaml.dump(content, sys.stdout)
        return

    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(content, file)


def main(input_file: str, output_file: str):
    logging.debug("Input file: %s", input_file)
    logging.debug("Output file: %s", output_file)

    yaml_content = read_yaml_file(input_file)
    logging.debug("Loaded YAML content: %s", pformat(dict(yaml_content)))

    if not output_file:
        logging.debug('No output file specified, writing to stdout')

    write_yaml_file(output_file, yaml_content)


if __name__ == "__main__":
    args = args_parser()

    main(args.input_file, args.output_file)
