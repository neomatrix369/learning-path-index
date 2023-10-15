#!/bin/bash

set -e
set -u
set -o pipefail

FULL_DOCKER_TAG_NAME="python-3.10-docker-env"
echo "Running image ${FULL_DOCKER_TAG_NAME}"; echo ""

# export GID=$(id -g)

WORKDIR="/home/"
LOCAL_MODEL_FOLDER="$(pwd)/../"
MODEL_VOLUME_SHARED="--volume ${LOCAL_MODEL_FOLDER}:${WORKDIR}"
OLLAMA_VOLUME_SHARED="--volume /usr/bin/ollama:/usr/bin/ollama"
HF_CACHE_SHARED="--volume ${LOCAL_MODEL_FOLDER}/.cache:/root/.cache"

set -x
time docker run --rm  -it --network="host" \
                --workdir "${WORKDIR}"     \
                ${HF_CACHE_SHARED}         \
                ${MODEL_VOLUME_SHARED}     \
                ${OLLAMA_VOLUME_SHARED}    \
                "${FULL_DOCKER_TAG_NAME}"
set +x

echo "* Finished running docker image ${FULL_DOCKER_TAG_NAME}"