# coding: utf-8
# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

"""
PYthon Dependencies vendOR
"""

__author__ = 'Jeremías Casteglione <jrmsdev@gmail.com>'
__license__ = 'BSD'
__version__ = '0.0'

import bottle
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

	_wapp = None

	def __init__(self):
		self._wapp = bottle.Bottle()

	def cmdArgs(self, parser):
		"""Set parser command line options."""
		p = parser.add_parser('proxy', help = 'pip proxy/cacher')
		p.set_defaults(command = 'proxy')
		p.add_argument('--host', help = 'bind to host name/address',
			default = 'localhost', metavar = 'localhost')
		p.add_argument('--port', help = 'bind to host port',
			type = int, default = 3737, metavar = 3737)

	def main(self, args):
		"""Proxy main method."""
		log.debug('proxy main')
		self.start(args.host, args.port, args.debug)
		return 0

	def start(self, host, port, debug):
		self._wapp.run(host = host, port = port, debug = debug,
			reloader = debug, quiet = not debug)

# command line args manager

class CmdArgs(object):
	"""Manage command line arguments."""

	_p = None

	def __init__(self):
		self._p = ArgumentParser(prog = 'pydor',
			description = 'PYthon Dependencies vendOR')
		self._p.add_argument('--version',
			action = 'version', version = '%(prog)s version ' + __version__)
		self._p.add_argument('--debug', action = 'store_true',
			default = False, help = 'enable all debug settings')
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
		return self._p.parse_args(args = argv)

	def printUsage(self):
		msg = self._p.format_usage()
		log.error(msg)

# global helper objects

log = None
path = Path()
config = Config()
proxy = Proxy()

# main

def main(argv = None):
	"""Main command entrypoint."""
	global log
	try:
		parser = CmdArgs()
		args = parser.parseArgs(argv)
		log = _logInit(args)
		log.debug('main')
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

def _logInit(args):
	if args.debug:
		args.log = 'debug'
	logFmt = '%(message)s'
	if args.log == 'debug':
		logFmt = '%(module)s:%(lineno)d: %(message)s'
	logging.basicConfig(format = logFmt, level = logging.WARNING)
	log = logging.getLogger('pydor')
	try:
		log.setLevel(args.log.upper())
	except ValueError:
		raise Error('ArgsError', f"invalid log level: {args.log}")
	return log

if __name__ == '__main__':
	sys.exit(main())
