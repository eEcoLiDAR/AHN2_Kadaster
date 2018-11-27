#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

POSTGIS_VERSION="${POSTGIS_VERSION%%+*}"

for DB in $(cat /db_list.txt); do
    echo "Updating PostGIS extensions '$DB' to $POSTGIS_VERSION"

    psql --dbname=$DB -c "
        CREATE EXTENSION IF NOT EXISTS postgis VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION postgis  UPDATE TO '$POSTGIS_VERSION';

        CREATE EXTENSION IF NOT EXISTS postgis_topology VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION postgis_topology UPDATE TO '$POSTGIS_VERSION';

        CREATE EXTENSION IF NOT EXISTS fuzzystrmatch VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION fuzzystrmatch UPDATE TO '$POSTGIS_VERSION';

		CREATE EXTENSION IF NOT EXISTS postgis_sfcgal VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION postgis_sfcgal UPDATE TO '$POSTGIS_VERSION';

		CREATE EXTENSION IF NOT EXISTS address_standardizer VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION address_standardizer UPDATE TO '$POSTGIS_VERSION';

        CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder VERSION '$POSTGIS_VERSION';
        ALTER EXTENSION postgis_tiger_geocoder UPDATE TO '$POSTGIS_VERSION';
    "
done
