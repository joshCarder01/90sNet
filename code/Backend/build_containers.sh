#!/bin/bash

# Build proxy
pushd ContainerNetwork
docker build -t proxy -f proxy.dockerfile .
popd

pushd ChallengeContainers
docker compose build
popd
