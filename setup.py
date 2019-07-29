#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import pydor
from setuptools import setup

deps = []
with open('requirements.txt', 'r') as fh:
	deps = fh.splitlines()

def main():
	setup(
		version = pydor.__version__,
		author = 'Jeremías Casteglione',
		author_email = 'jrmsdev@gmail.com',
		python_requires = '~=3.6',
		setup_requires = ['wheel>=0.33'],
		install_requires = deps,
		py_modules = ['pydor'],
		test_suite = 'pydor_test',
	)

if __name__ == '__main__':
	main()
