#!/bin/sh
set -eu
(cd docs && make html BUILDDIR=_build)
exit 0
