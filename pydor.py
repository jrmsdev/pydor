# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys

from configparser import ConfigParser, ExtendedInterpolation

__all__ = ['main']

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

# helper objects

config = _Config()

# main

def main():
	return 0

if __name__ == '__main__':
	sys.exit(main())
