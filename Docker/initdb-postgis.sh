#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

for DB in $(cat /db_list.txt); do
	echo "Creating a database for tile " $DB
	createdb $DB

	echo "Loading PostGIS extensions into $DB"
    psql --dbname=$DB -c "
        CREATE EXTENSION IF NOT EXISTS postgis;
        CREATE EXTENSION IF NOT EXISTS postgis_topology;
		CREATE EXTENSION IF NOT EXISTS postgis_sfcgal;
		CREATE EXTENSION IF NOT EXISTS address_standardizer;
        CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
		CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
    "
done
