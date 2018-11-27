# AHN2_Kadaster
Enrich AHN2 with Kadaster classesd


# PostGIS server

## Install docker
Follow instructions to install docker.


## Create a docker volume

sudo systemctl stop docker
sudo mkdir /data/local/docker-data
sudo vim /etc/docker/daemon.json
<!-- add the lines below -->
{
	"data-root": "/data/local/docker-data"
}

<!-- Create a Docker volume in /data/local/postgis-data:
sudo docker volume create --name postgis-data -o type=btrfs  -o o=bind -->


## Start the server
docker run -d --name eecolidar-postgis -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v postgis-data:/var/lib/postgresql fdiblen/eecolidar-postgis


## Setup the firewall
sudo ufw allow 5432/tcp



## Local Postresql installation

docker pull postgres
docker run --rm -ti postgres /usr/bin/psql

For get help about psql:
docker run --rm -ti postgres /usr/bin/psql --help

## Test
psql -h localhost -p 5432 -U postgres

password is **mysecretpassword**

to list databases:
\l or \list

to connect to a database:
\c database_name or \connect database_name

to show tables in database_name:
\dt+

to query data in a table:
SELECT * FROM table_name;
or
SELECT column, column2….
FROM table;

to count rows:
SELECT COUNT (*)
FROM table_name;


## Check database extensions

\connect mygisdb
\x
\dx postgis*


## GML file info
to show basic info:
ogrinfo -fields=YES  TOP10NL_01O.gml

to show all the layers and features:
ogrinfo -fields=YES -al TOP10NL_01O.gml

## Download top10NL data

https://www.pdok.nl/downloads?articleid=1976855
[Direct link](http://geodata.nationaalgeoregister.nl/top10nlv2/extract/kaartbladtotaal/top10nl.zip?formaat=gml)


## convert GML to CSV

ogr2ogr -f "CSV" Top10NL_000001.csv Top10NL_000001.gml


## import GML file to the server

ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres dbname=eecolidar password=mysecretpassword" Top10NL_000001.gml

with a new table

ogr2ogr -f "PostgreSQL" PG:"host=localhost user=postgres dbname=template_postgis password=mysecretpassword" Top10NL_000001.gml -nln newtablename