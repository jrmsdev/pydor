#!/bin/sh
set -eu
PYTHONPATH=${PWD} pytest --cov=. --cov-report=html --cov-report=term $@
exit 0
