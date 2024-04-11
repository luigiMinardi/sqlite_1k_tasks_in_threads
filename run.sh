#!/usr/bin/env bash

if [ ! -d .venv ] ; then
    python -m venv .venv
fi
source .venv/bin/activate
echo "Installing missing dependecies if needed."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt --ignore-installed > /dev/null
./main.py
