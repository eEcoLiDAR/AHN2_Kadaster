#!/bin/bash

docker build --tag eecolidar-postgis --label eecolidar-postgis .

## to run:
## docker run --rm -ti --name eecolidar-postgis -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432  eecolidar-postgis


## to push:
## docker tag eecolidar-postgis $DOCKER_ID_USER/eecolidar-postgis
## docker push $DOCKER_ID_USER/eecolidar-postgis