# coding: utf-8
# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

"""
PYthon Dependencies vendOR
"""

__author__ = 'Jeremías Casteglione <jrmsdev@gmail.com>'
__license__ = 'BSD'
__version__ = '0.0'

import logging
import sys

from configparser import ConfigParser, ExtendedInterpolation
from os import path as ospath

__all__ = (
	'Error',
	'Log',
	'Path',
	'Config',
	'main',
)

# error class

class Error(Exception):
	"""Exception class for raising errors."""
	pass

# logger class

class Log(object):
	"""Logger class.

	Default level: WARNING
	"""

	_log = None

	def __init__(self):
		self._log = logging.getLogger('pydor')
		self._log.setLevel('WARNING')

	def error(self, msg, *args):
		"""Error messages."""
		msg = 'ERROR: ' + msg
		self._log.error(msg, *args)

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

log = Log()
path = Path()
config = Config()

# main

def main(filename = 'pydor.ini'):
	"""Main command entrypoint."""
	try:
		config.read(filename = filename)
	except Error as err:
		log.error('ERROR: %s', err)
		return 1
	return 0

if __name__ == '__main__':
	sys.exit(main()) # pragma: no cover
