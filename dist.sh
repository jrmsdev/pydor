#!/bin/sh
set -eu
UPLOAD=${1:-'none'}
./setup.py clean
./setup.py dist
if test "${UPLOAD}" = 'upload'; then
	twine upload -s -i jrmsdev@gmail.com dist/pydor-*.*
fi
exit 0
