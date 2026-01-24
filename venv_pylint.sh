#!/bin/bash

set -eu

VENV_DIR="$(dirname $0)/.venv"

if [ ! -d "${VENV_DIR}" ]
then
    echo "Missing venv directory, run venv_setup.sh"
    exit 1
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# shellcheck disable=SC2046
pylint $(git ls-files '*.py')
