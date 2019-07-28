#!/bin/sh
set -eu
TAG=${1:-''}
IMAGE='jrmsdev/pydor'
NAME='pydor'
if test "X${TAG}" != 'X'; then
	shift
	IMAGE="jrmsdev/pydor:${TAG}"
	NAME="pydor${TAG}"
fi
docker run -it --rm -u pydor \
	--name=${NAME} \
	--hostname=${NAME} \
	-v ${PWD}:/home/pydor/src \
	${IMAGE} $@
exit 0
