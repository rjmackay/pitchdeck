#!/bin/sh
wait-for-it $DB_HOST:$DB_PORT

pipenv run "$@"
