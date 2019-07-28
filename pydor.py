# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys

from configparser import ConfigParser, ExtendedInterpolation
from os import path as ospath

__all__ = ['main']

# error class

class Error(Exception):
	pass

# filesystem paths manager

class _Path(object):

	def join(self, *parts):
		return ospath.join(*parts)

# config manager

_ConfigDefault = {
	'requirements': 'requirements.txt',
}

class _Config(object):
	_cfg = None

	def __init__(self):
		self._cfg = ConfigParser(defaults = {},
			allow_no_value = False,
			delimiters = ('=',),
			comment_prefixes = ('#',),
			strict = True,
			interpolation = ExtendedInterpolation(),
			default_section = 'default')
		self._cfg['default'] = _ConfigDefault

	def read(self):
		ok = self._cfg.read('pydor.ini')
		if len(ok) < 1:
			raise Error('pydor.ini config file not found')

# helper objects

path = _Path()
config = _Config()

# main

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
