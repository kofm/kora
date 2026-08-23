#!/bin/sh

set -eu

: "${DB_HOST:?DB_HOST is required}"
: "${DB_PORT:?DB_PORT is required}"
: "${DB_NAME:?DB_NAME is required}"
: "${DB_USER:?DB_USER is required}"
: "${DB_PASSWORD:?DB_PASSWORD is required}"

printf '%s\n' "Collect static files"
uv run --no-dev manage.py collectstatic --noinput --clear

printf '%s\n' "Refresh documentation"
rm -rf /var/www/docs/*
cp -a /opt/kora-docs/html/. /var/www/docs/

printf '%s\n' "Apply database migrations"
uv run --no-dev manage.py migrate --noinput

cat << "EOF"
 ___  __    ________  ________  ________
|\  \|\  \ |\   __  \|\   __  \|\   __  \
\ \  \/  /|\ \  \|\  \ \  \|\  \ \  \|\  \
 \ \   ___  \ \  \\\  \ \   _  _\ \   __  \
  \ \  \\ \  \ \  \\\  \ \  \\  \\ \  \ \  \
   \ \__\\ \__\ \_______\ \__\\ _\\ \__\ \__\
    \|__| \|__|\|_______|\|__|\|__|\|__|\|__|
EOF

exec "$@"
