#!/bin/sh
set -eu
(cd docs && make dirhtml BUILDDIR=.)
exit 0
