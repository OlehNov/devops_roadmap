#!/bin/sh

# Wait for the db to be available!
./wait-for-it.sh back:8000 --timeout=60 --strict -- echo "Backend is up"
