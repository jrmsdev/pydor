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

from argparse import ArgumentParser
from configparser import ConfigParser, ExtendedInterpolation
from os import path as ospath

__all__ = (
	'ErrorType',
	'Error',
	'Path',
	'Config',
	'CmdArgs',
	'main',
)

# errors manager

@enum.unique
class ErrorType(enum.Enum):
	"""Map error types with exit return status."""
	ConfigError = 10
	ArgsError = 11

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
		self._readFiles = self._cfg.read(('setup.cfg', filename))

# command line args manager

class CmdArgs(ArgumentParser):
	"""Manage command line arguments."""

	def __init__(self):
		super().__init__(prog = 'pydor', description = 'PYthon Dependencies vendOR')
		self.add_argument('--version',
			action = 'version', version = '%(prog)s version ' + __version__)
		self.add_argument('--log', help = 'set log level (default: warning)',
			default = 'warning', metavar = 'level')

	def parse_args(self, argv):
		"""Parse command args, then set log level from parsed options."""
		x = super().parse_args(args = argv)
		try:
			log.setLevel(x.log.upper())
		except ValueError:
			raise Error('ArgsError', f"invalid log level: {x.log}")
		return x

# global helper objects

log = logging.getLogger('pydor')
path = Path()
config = Config()

# main

def main(argv = None):
	"""Main command entrypoint."""
	try:
		cmd = CmdArgs()
		args = cmd.parse_args(argv)
		config.read()
	except Error as err:
		log.error(err)
		return err.status
	return 0

if __name__ == '__main__':
	sys.exit(main())
