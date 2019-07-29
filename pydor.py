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
	'CmdArgs',
	'Config',
	'Error',
	'ErrorType',
	'Path',
	'Proxy',
	'main',
)

# errors manager

@enum.unique
class ErrorType(enum.Enum):
	"""Map error types with exit return status."""
	ArgsError = 10

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

# pip proxy manager

class Proxy(object):
	"""Pip proxy/cacher manager."""

	def cmdArgs(self, parser):
		"""Set parser command line options."""
		p = parser.add_parser('proxy', help = 'pip proxy/cacher')
		p.set_defaults(command = 'proxy')

	def main(self, args):
		"""Proxy main method."""
		return 0

# command line args manager

class CmdArgs(object):
	"""Manage command line arguments."""

	_p = None

	def __init__(self):
		self._p = ArgumentParser(prog = 'pydor',
			description = 'PYthon Dependencies vendOR')
		self._p.add_argument('--version',
			action = 'version', version = '%(prog)s version ' + __version__)
		self._p.add_argument('--log', help = 'set log level (default: warning)',
			default = 'warning', metavar = 'level')
		self.addSubparsers()

	def addSubparsers(self):
		"""Add a subparser with options for sub commands."""
		p = self._p.add_subparsers(title = 'commands',
			description = 'run `pydor command -h` for more information',
			help = 'description')
		proxy.cmdArgs(p)

	def parseArgs(self, argv):
		"""Parse command args, then set log level from parsed options."""
		x = self._p.parse_args(args = argv)
		try:
			log.setLevel(x.log.upper())
		except ValueError:
			raise Error('ArgsError', f"invalid log level: {x.log}")
		return x

	def printUsage(self):
		self._p.print_usage()

# global helper objects

log = logging.getLogger('pydor')
path = Path()
config = Config()
proxy = Proxy()

# main

def main(argv = None):
	"""Main command entrypoint."""
	try:
		parser = CmdArgs()
		args = parser.parseArgs(argv)
		config.read()
		try:
			cmd = args.command
		except AttributeError:
			parser.printUsage()
			return 1
		if cmd == 'proxy':
			return proxy.main(args)
	except Error as err:
		log.error(err)
		return err.status
	# not reached
	return 99 # pragma: no cover

if __name__ == '__main__':
	sys.exit(main())
