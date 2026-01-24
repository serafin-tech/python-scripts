#!/bin/bash

set -eu

VENV_DIR="$(dirname $0)/.venv"

if [ ! -d "${VENV_DIR}" ]
then
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python3 -m pip install -U pip
python3 -m pip install -e .[dev]
