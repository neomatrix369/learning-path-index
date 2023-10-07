#!/bin/bash

set -e
set -u
set -o pipefail

cleanup() {
	containersToRemove=$(docker ps --quiet --filter "status=exited")
	[ ! -z "${containersToRemove}" ] && \
	    echo "Remove any stopped container from the local registry" && \
	    docker rm ${containersToRemove} || true

	imagesToRemove=$(docker images --quiet --filter "dangling=true")
	[ ! -z "${imagesToRemove}" ] && \
	    echo "Remove any dangling images from the local registry" && \
	    docker rmi -f ${imagesToRemove} || true
}

FULL_DOCKER_TAG_NAME="python-3.10-docker-env"
echo "Building image ${FULL_DOCKER_TAG_NAME}"; echo ""

WORKDIR="/home/"
cleanup

# cp ../requirements.txt .
set -x
time docker build                              \
                --build-arg WORKDIR=${WORKDIR} \
                -t ${FULL_DOCKER_TAG_NAME}     \
                .
set +x

echo "* Finished building docker image ${FULL_DOCKER_TAG_NAME}"

cleanup