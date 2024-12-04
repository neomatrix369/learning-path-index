# #!/bin/bash

# set -e
# set -u
# set -o pipefail

# DOCKER_USER_NAME="$(whoami)"
# FULL_DOCKER_TAG_NAME="${FULL_DOCKER_TAG_NAME:-python-3.10-docker-env:latest}"
# echo "Running image ${FULL_DOCKER_TAG_NAME}"; echo ""
# echo "FULL_DOCKER_TAG_NAME: ${FULL_DOCKER_TAG_NAME}"

# # pullImage() {
# # 	FULL_DOCKER_TAG_NAME="${DOCKER_USER_NAME}/${FULL_DOCKER_TAG_NAME}"

# # 	docker pull ${FULL_DOCKER_TAG_NAME} || true
# # }

# WORKDIR="/home/"
# LOCAL_MODEL_FOLDER="$(pwd)/../"
# MODEL_VOLUME_SHARED="--volume ${LOCAL_MODEL_FOLDER}:${WORKDIR}"
# OLLAMA_VOLUME_SHARED="--volume $(which ollama):/usr/bin/ollama"
# HF_CACHE_SHARED="--volume ${LOCAL_MODEL_FOLDER}/.cache:/root/.cache"

# set -x

# # pullImage
# time docker run --rm  -it \
#                 #--platform="linux/amd64"   \
#                 --network="host"           \
#                 --add-host=host.docker.internal:host-gateway \
#                 --workdir "${WORKDIR}"     \
#                 --env OLLAMA_HOST="http://host.docker.internal:11434" \
#                 ${HF_CACHE_SHARED}         \
#                 ${MODEL_VOLUME_SHARED}     \
#                 ${OLLAMA_VOLUME_SHARED}    \
#                 python-3.10-docker-env:latest
# set +x

# echo "* Finished running docker image ${FULL_DOCKER_TAG_NAME}"



#!/bin/bash

set -e
set -u
set -o pipefail

DOCKER_USER_NAME="$(whoami)"
FULL_DOCKER_TAG_NAME="${FULL_DOCKER_TAG_NAME:-python-3.10-docker-env:latest}"
echo "Running image: '${FULL_DOCKER_TAG_NAME}'"; echo ""

WORKDIR="/home/"
LOCAL_MODEL_FOLDER="$(pwd)/../"
MODEL_VOLUME_SHARED="--volume ${LOCAL_MODEL_FOLDER}:${WORKDIR}"
OLLAMA_VOLUME_SHARED="--volume $(which ollama):/usr/bin/ollama"
HF_CACHE_SHARED="--volume ${LOCAL_MODEL_FOLDER}/.cache:/root/.cache"

set -x

time docker run --rm -it \
    --network="host" \
    --add-host=host.docker.internal:host-gateway \
    --workdir="${WORKDIR}" \
    --env OLLAMA_HOST="http://host.docker.internal:11434" \
    ${HF_CACHE_SHARED} \
    ${MODEL_VOLUME_SHARED} \
    ${OLLAMA_VOLUME_SHARED} \
    "${FULL_DOCKER_TAG_NAME}"

set +x

echo "* Finished running docker image: '${FULL_DOCKER_TAG_NAME}'"