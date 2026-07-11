#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
killall python3
cd ${SCRIPT_DIR}
(sleep 2; firefox -url 127.0.0.1:5000 -fullscreen) &
KEFIL_PRINTER=/dev/usb/lp1 venv/bin/python3 app.py 2>&1 | tee -a logs.txt
