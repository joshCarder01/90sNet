#!/bin/bash

# Build proxy
#docker build -t proxy:local -f ./DockerFiles/proxy.dockerfile ./ContainerNetwork
docker build -t proxy:local -f ./DockerFiles/proxy.dockerfile ./DockerFiles/

pushd ChallengeContainers
docker compose build
popd
