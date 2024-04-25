#!/bin/bash

set -e
set -u
set -o pipefail

DOCKER_USER_NAME="neomatrix369"
FULL_DOCKER_TAG_NAME="python-3.10-docker-env"
echo "Running image ${FULL_DOCKER_TAG_NAME}"; echo ""

pullImage() {
	FULL_DOCKER_TAG_NAME="${DOCKER_USER_NAME}/${FULL_DOCKER_TAG_NAME}"

	docker pull ${FULL_DOCKER_TAG_NAME} || true
}

WORKDIR="/home/"
LOCAL_MODEL_FOLDER="$(pwd)/../"
MODEL_VOLUME_SHARED="--volume ${LOCAL_MODEL_FOLDER}:${WORKDIR}"
OLLAMA_VOLUME_SHARED="--volume $(which ollama):/usr/bin/ollama"
HF_CACHE_SHARED="--volume ${LOCAL_MODEL_FOLDER}/.cache:/root/.cache"

set -x
pullImage
time docker run --rm -it                   \
                --platform="linux/amd64"   \
                --network="host"           \
                --workdir "${WORKDIR}"     \
                ${HF_CACHE_SHARED}         \
                ${MODEL_VOLUME_SHARED}     \
                ${OLLAMA_VOLUME_SHARED}    \
                "${FULL_DOCKER_TAG_NAME}"
set +x

echo "* Finished running docker image ${FULL_DOCKER_TAG_NAME}"