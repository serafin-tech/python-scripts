#!/bin/bash

docker run --rm -it -v $PWD:$PWD cliapp:latest --help
