#!/bin/sh -eu
REPORT=${1:-'html'}
PYTHONPATH=${PWD} pytest --cov=. --cov-report=${REPORT}
exit 0
