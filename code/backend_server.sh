#!/bin/bash
# script for starting backend manager
cd Backend
docker-compose build
docker-compose up &
sleep 5

cd ..