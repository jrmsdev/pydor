# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from os import getcwd, path, chdir
from unittest import TestCase, main

import pydor
import pytest

_srcdir = path.abspath(getcwd())

# set logger to only show critical messages

pydor.log._log.setLevel('CRITICAL')

# setUp / tearDown testing env

def _setUp(env):
	envdir = path.join(_srcdir, 'testdata', env.replace('/', path.sep))
	chdir(envdir)

def _tearDown(env):
	chdir(_srcdir)

# test pydor.path

class TestPath(TestCase):

	def test_join(t):
		assert pydor.path.join('p1', 'p2') == path.join('p1', 'p2')

# test pydor.config

class TestConfig(TestCase):

	def setUp(t):
		_setUp('config')

	def tearDown(t):
		_tearDown('config')

	def test_default(t):
		assert isinstance(pydor.config, pydor.Config)
		assert isinstance(pydor.config._cfg, ConfigParser)
		assert pydor.config._cfg.defaults() == {
			'requirements': 'requirements.txt',
		}
		assert pydor.config._cfg.sections() == []

	def test_read(t):
		pydor.config.read()

	def test_read_error(t):
		with pytest.raises(pydor.Error, match = 'config file not found'):
			pydor.config.read(filename = 'nofile.ini')

# test pydor commands

class TestPydor(TestCase):

	def setUp(t):
		_setUp('cmd/main')

	def tearDown(t):
		_tearDown('cmd/main')

	def test_main(t):
		assert pydor.main() == 0

	def test_main_cfg_error(t):
		assert pydor.main(filename = 'nofile.ini') == 1

# main

if __name__ == '__main__':
	main()
