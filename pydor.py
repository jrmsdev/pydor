# coding: utf-8
# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

"""
PYthon Dependencies vendOR
"""

__author__ = 'Jeremías Casteglione <jrmsdev@gmail.com>'
__license__ = 'BSD'
__version__ = '0.0'

import enum
import logging
import sys

from configparser import ConfigParser, ExtendedInterpolation
from os import path as ospath

__all__ = (
	'ErrorType',
	'Error',
	'Path',
	'Config',
	'main',
)

# errors manager

@enum.unique
class ErrorType(enum.Enum):
	"""Map error types with exit return status."""
	ConfigError = 10

class Error(Exception):
	"""Base class for raising errors."""

	_msg = None
	_typ = None
	status = None

	def __init__(self, typ, msg):
		self._msg = str(msg)
		self._typ = ErrorType[typ].name
		self.status = ErrorType[typ].value

	def __str__(self):
		return f"{self._typ}: {self._msg}"

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
	_readFiles = None

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
		self._readFiles = self._cfg.read(['setup.cfg', filename])

# helper objects

log = logging.getLogger('pydor')
path = Path()
config = Config()

# main

def main():
	"""Main command entrypoint."""
	try:
		log.setLevel('WARNING')
		config.read()
	except Error as err:
		log.error(err)
		return err.status
	return 0

if __name__ == '__main__':
	sys.exit(main()) # pragma: no cover
