#!/bin/sh -eu
REPORT=${1:-'term'}
PYTHONPATH=${PWD} pytest --cov=. --cov-report=${REPORT}
exit 0
