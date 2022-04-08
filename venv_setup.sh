#!/bin/bash

if [ ! -d venv ]
then
    python3 -m venv venv
fi

. venv/bin/activate

pip3 install -r requirements.txt
