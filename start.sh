#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
killall /home/diwan/kefil-main/venv/bin/python3
cd ${SCRIPT_DIR}
(sleep 3; /usr/bin/chromium --new-window --no-default-browser-check --allow-insecure-localhost --no-first-run --disable-sync --start-maximized --app=http://127.0.0.1:5000) &
venv/bin/python3 app.py 2>&1 | tee -a logs.txt

