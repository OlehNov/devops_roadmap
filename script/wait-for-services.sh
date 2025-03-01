#!/bin/bash

services=("db:3306" "broker:6379" "web:8000")

TIMEOUT=120

for service in "${services[@]}"; do
  host=$(echo $service | cut -d':' -f1)
  port=$(echo $service | cut -d':' -f2)

  echo "Waiting for $host:$port..."

  start_time=$(date +%s)
  while ! nc -z $host $port; do
    sleep 2
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ $elapsed_time -ge $TIMEOUT ]; then
      echo "Timeout: $host:$port is not available after $TIMEOUT seconds. Exiting..."
      exit 1
    fi
  done

  echo "$host:$port is available!"
done

exec /bin/sh /app/script/docker-entrypoint.sh
