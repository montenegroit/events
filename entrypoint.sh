#!/bin/sh

if [[ ${db_host} ]]; then
    export PGPASSWORD=${db_pass}
    until psql -h $db_host -U $db_user -c '\l'; do
      >&2 echo "Postgres is unavailable - sleeping 63 sec"
      sleep 63
    done
    >&2 echo "Postgres is up - continuing"
    unset PGPASSWORD
fi

echo "Running migrations"
alembic upgrade head
echo "Migrations set"
uvicorn src.main:app --host 0.0.0.0 --port 8000

exec "$@"

