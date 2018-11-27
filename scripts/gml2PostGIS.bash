#!/bin/bash

COUNTER=0

for file in $(ls $PWD/*.gml)
do
    COUNTER=$[$COUNTER +1]
    baseName=$(basename $file .gml)
    tileID=$(echo $baseName | cut -d'_' -f2)
    dbName='Tile'$tileID

    echo
    echo $COUNTER': ' $file
    echo 'Processing tile ' $tileID
    
    ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres  password=mysecretpassword dbname=$dbName" $file
done