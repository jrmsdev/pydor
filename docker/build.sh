#!/bin/sh
set -eu
TAG=${1:-''}
IMAGE='jrmsdev/pydor'
DOCKERFN='Dockerfile'
if test "X${TAG}" != "X"; then
	IMAGE="jrmsdev/pydor:${TAG}"
	DOCKERFN="Dockerfile.${TAG}"
fi
docker build \
	--build-arg PYDOR_UID=$(id -u) \
	--build-arg PYDOR_GID=$(id -g) \
	-t ${IMAGE} -f docker/${DOCKERFN} .
exit 0
