#!/bin/sh
set -eu
if which check-manifest >/dev/null; then
	check-manifest
fi
./setup.py check
./setup.py test
exit 0
