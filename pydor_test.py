# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from unittest import TestCase, main
from os import getcwd, path, chdir

import pydor

_srcdir = path.abspath(getcwd())

# setUp / tearDown testing env

def _setUp(env):
	envdir = path.join(_srcdir, 'testdata', env)
	chdir(envdir)

def _tearDown(env):
	chdir(_srcdir)

# test pydor

class TestPydor(TestCase):

	def test_fake(t):
		assert True

# test pydor.config

class TestConfig(TestCase):

	def setUp(t):
		_setUp('config')

	def tearDown(t):
		_tearDown('config')

	def test_default(t):
		assert isinstance(pydor.config, pydor._Config)
		assert isinstance(pydor.config._cfg, ConfigParser)
		assert pydor.config._cfg.defaults() == {
			'requirements': 'requirements.txt',
		}
		assert pydor.config._cfg.sections() == []

	def test_read(t):
		pydor.config.read()

# main

if __name__ == '__main__':
	main()
