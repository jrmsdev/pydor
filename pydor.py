# coding: utf-8
# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

"""
PYthon Dependencies vendOR
"""

__all__ = (
	'Error',
	'Path',
	'Config',
	'main',
)

__author__ = 'Jeremías Casteglione <jrmsdev@gmail.com>'
__version__ = 0.0
__license__ = 'BSD'

import sys

from configparser import ConfigParser, ExtendedInterpolation
from os import path as ospath

# error class

class Error(Exception):
	"""Exception class for raising errors."""
	pass

# filesystem paths manager

class Path(object):
	"""Manage filesystem paths."""

	def join(self, *parts):
		"""Join name parts."""
		return ospath.join(*parts)

# config manager

ConfigDefault = {
	'requirements': 'requirements.txt',
}

class Config(object):
	"""Manage main configuration."""
	_cfg = None

	def __init__(self):
		self._cfg = ConfigParser(defaults = {},
			allow_no_value = False,
			delimiters = ('=',),
			comment_prefixes = ('#',),
			strict = True,
			interpolation = ExtendedInterpolation(),
			default_section = 'default')
		self._cfg['default'] = ConfigDefault

	def read(self, filename = 'pydor.ini'):
		"""Read configuration file."""
		ok = self._cfg.read(filename)
		if len(ok) < 1:
			raise Error(f"{filename} config file not found")

# helper objects

path = Path()
config = Config()

# main

def main(filename = 'pydor.ini'):
	"""Main function for command entrypoint."""
	try:
		config.read(filename = filename)
	except Error as err:
		print('ERROR:', err, file = sys.stderr)
		return 1
	return 0

if __name__ == '__main__': # pragma: no cover
	sys.exit(main())
