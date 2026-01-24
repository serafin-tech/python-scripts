#!/bin/bash

set -eu

VENV_DIR="$(dirname $0)/.venv"

if [[ ! -d "${VENV_DIR}" ]]
then
  python3.12 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

python3.12 -m pip install -U pip
python3.12 -m pip install -U .[dev]

python3.12 -m pip install -U build setuptools setuptools-scm

rm -rf dist/ *.egg-info/

python3.12 -m build .

docker buildx build . -t cliapp:latest
