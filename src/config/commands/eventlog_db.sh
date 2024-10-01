#!/bin/bash

mysql -u ${MYSQL_USER} -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${EVENTLOGS_DATABASE};" && tail -f /dev/null