#!/bin/bash

if [[ ! -d venv ]]
then
  python3.12 -m venv venv
fi

source venv/bin/activate

python3.12 -m pip install -U pip
python3.12 -m pip install -U -r requirements.txt

python3.12 -m pip install -U build setuptools setuptools-scm

rm -rf dist/ *.egg-info/

python3.12 -m build .

docker buildx build . -t cliapp:latest
