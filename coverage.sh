#!/bin/sh
REPORT=${COVFMT}
if test -z "${REPORT}"; then
	REPORT='html'
fi
PYTHONPATH=${PWD} pytest --cov=. --cov-report=${REPORT} $@
