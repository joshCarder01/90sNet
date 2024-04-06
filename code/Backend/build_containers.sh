#!/bin/bash

# Build proxy
docker build -t proxy:local -f ./DockerFiles/proxy.dockerfile ./ContainerNetwork

pushd ChallengeContainers
docker compose build
popd
