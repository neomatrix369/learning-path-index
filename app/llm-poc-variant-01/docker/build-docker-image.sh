#!/bin/bash

set -e
set -u
set -o pipefail

DOCKER_USER_NAME="${DOCKER_USER_NAME:-neomatrix369}"
FULL_DOCKER_TAG_NAME="python-3.10-docker-env"

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

pushImageToHub() {
	echo "Pushing image ${FULL_DOCKER_TAG_NAME} to Docker Hub"; echo ""

	docker login --username=${DOCKER_USER_NAME}
	pushImage ${FULL_DOCKER_TAG_NAME}
}

findImage() {
	IMAGE_NAME="${1}"
	echo $(docker images ${IMAGE_NAME} -q | head -n1 || true)
}

pushImage() {
	IMAGE_NAME="${1}"
	FULL_DOCKER_TAG_NAME="${DOCKER_USER_NAME}/${IMAGE_NAME}"

	IMAGE_FOUND="$(findImage ${IMAGE_NAME})"
	IS_FOUND="found"
	if [[ -z "${IMAGE_FOUND}" ]]; then
		IS_FOUND="not found"
	fi
	echo "Docker image '${DOCKER_USER_NAME}/${IMAGE_NAME}' is ${IS_FOUND} in the local repository"

	docker tag ${IMAGE_FOUND} ${FULL_DOCKER_TAG_NAME}
	docker push ${FULL_DOCKER_TAG_NAME}
}


echo "Building image ${FULL_DOCKER_TAG_NAME}"; echo ""

WORKDIR="/home/"
cleanup

cp ../requirements.txt .
set -x
time docker build                              \
                --build-arg WORKDIR=${WORKDIR} \
                -t ${FULL_DOCKER_TAG_NAME}     \
                .
set +x
rm -f requirements.txt

echo "* Finished building docker image ${FULL_DOCKER_TAG_NAME}"

pushImageToHub

cleanup