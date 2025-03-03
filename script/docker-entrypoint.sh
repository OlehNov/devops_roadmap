#!/bin/sh

host="db"
port="3306"
timeout=60
elapsed=0

echo "Waiting for database to be ready..."
until mysqladmin ping -h"${DB_HOST}" -P"${DB_PORT}" -u"${DB_USER}" -p"${DB_PASSWORD}" --silent; do
  echo "Database is unavailable - sleeping"
  sleep 1
  elapsed=$((elapsed + 1))

  if [ "$elapsed" -ge "$timeout" ]; then
    echo "Error: Database did not become available within $timeout seconds"
    exit 1
  fi
done

echo "Database is up - executing commands"
python src/addons/databases/create_eventlog_db_script.py
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py migrate eventlogs --database=eventlog
exec python src/manage.py runserver 0.0.0.0:8000

# host="db"
# port="3306"
# timeout=60
# elapsed=0

# echo "Waiting for database to be ready..."
# until mysqladmin ping -h"$host" -P"$port" --silent; do
#   echo "Database is unavailable - sleeping"
#   sleep 1
#   elapsed=$((elapsed + 1))

#   if [ "$elapsed" -ge "$timeout" ]; then
#     echo "Error: Database did not become available within $timeout seconds"
#     exit 1
#   fi
# done

# echo "Database is up - executing commands"
# python src/addons/databases/create_eventlog_db_script.py
# python src/manage.py makemigrations
# python src/manage.py migrate
# python src/manage.py migrate eventlogs --database=eventlog
# # python src/manage.py loaddata src/dump.json
# exec python src/manage.py runserver 0.0.0.0:8000
