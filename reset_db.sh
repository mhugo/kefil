#!/usr/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DB_FILE=${SCRIPT_DIR}/orders.db
rm -f ${DB_FILE}
sqlite3 ${DB_FILE} < ${SCRIPT_DIR}/sql/init.sql
sqlite3 ${DB_FILE} < ${SCRIPT_DIR}/sql/config.sql
sqlite3 ${DB_FILE} < ${SCRIPT_DIR}/sql/sample.sql
