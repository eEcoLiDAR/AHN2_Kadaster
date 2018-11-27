#!/bin/bash

echo > tile_list.txt

for file in $(ls $PWD/*.gml)
do
    baseName=$(basename $file .gml)
    tileID=$(echo $baseName | cut -d'_' -f2)

    echo
    echo 'Processing tile ' $tileID
    echo 'Tile'$tileID >> tile_list.txt

    mkdir -p $tileID
    ogrinfo -fields=YES $file > $tileID'/layers.txt'
    ogrinfo -fields=YES -al $file > $tileID'/features.txt'
    ogr2ogr  --debug ON -f "CSV" $tileID'/'$tileID'.csv' $file 

# -lco GEOMETRY=AS_XYZ
# -t_srs "EPSG:4326" 
# -t_srs is the “target spatial reference system”, telling ogr2ogr to convert the spatial coordinates to “EPSG:4326” (WGS84)
done