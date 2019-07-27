#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from setuptools import setup

def main():
	setup(
		version = '0.0',
		author = 'Jeremías Casteglione',
		author_email = 'jrmsdev@gmail.com',
		python_requires = '~=3.6',
		setup_requires = ['wheel>=0.33'],
		install_requires = [],
		py_modules = ['pydor'],
	)

if __name__ == '__main__':
	main()
