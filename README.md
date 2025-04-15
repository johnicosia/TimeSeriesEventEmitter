# TimeSeriesEventEmitter
Interview Exercise

# Requirements
python3 with the following dependencies:
    pip3 install FastAPI
    pip3 install uvicorn
    pip3 install influxdb-client

docker - using influxdb's offical docker image

# Run influxdb using docker
This is the command to setup a docker container with influxdb note that if any of the values are different here main.py needs to be updated starting on (line 11) for the following properties:
bucket = "test"
org = "test"
token = "HLA5J8IhE_TAQjAoXX8buquu49a6tpofyXNs26RfWNtTNJXpnfox2zwgBSEeKTP7ggb6G55xJrZaupDVKGBkSg=="
url="http://localhost:8086"

docker run \
 --name influxdb2 \
 --publish 8086:8086 \
 --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
 --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
 --env DOCKER_INFLUXDB_INIT_MODE=setup \
 --env DOCKER_INFLUXDB_INIT_USERNAME=admin \
 --env DOCKER_INFLUXDB_INIT_PASSWORD=admin1234 \
 --env DOCKER_INFLUXDB_INIT_ORG=test \
 --env DOCKER_INFLUXDB_INIT_BUCKET=test \
 influxdb:2

The command to normally run the docker container
docker start influxdb2

# Run server
python3 main.py