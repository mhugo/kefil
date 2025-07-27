#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
killall /home/diwan/kefil-main/venv/bin/python3
cd ${SCRIPT_DIR}
(sleep 3; firefox http://localhost:5000) &
venv/bin/python3 app.py
