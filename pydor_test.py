# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from os import getcwd, path, chdir
from subprocess import call as cmdrun
from unittest import TestCase, main

import pydor
import pytest

_srcdir = path.abspath(getcwd())

# mock pydor.log

pydor.log.setLevel('CRITICAL')

class MockLog(object):

	def setLevel(self, level):
		pass

	def error(self, msg, *args):
		pass

del pydor.log
pydor.log = MockLog()

# setUp / tearDown testing env

def _setUp(env):
	envdir = path.join(_srcdir, 'testdata', env.replace('/', path.sep))
	chdir(envdir)

def _tearDown(env):
	chdir(_srcdir)

# test errors management

class TestError(TestCase):

	def test_default(t):
		err = pydor.Error('ConfigError', 'testing')
		assert err._typ == 'ConfigError'
		assert err.status == 10
		assert err.status == pydor.ErrorType.ConfigError.value
		assert str(err) == 'ConfigError: testing'

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
		assert pydor.config._readFiles == ['pydor.ini']
		assert pydor.config._cfg.has_section('pydor')

	def test_other_files(t):
		try:
			_setUp('config.other_files')
			pydor.config.read()
			assert pydor.config._readFiles == ['setup.cfg']
			assert pydor.config._cfg.has_section('pydor')
		finally:
			_tearDown('config.other_files')

# test pydor commands

class TestMain(TestCase):

	def setUp(t):
		_setUp('cmd/main')

	def tearDown(t):
		_tearDown('cmd/main')

	def test_main(t):
		assert pydor.main([]) == 0

	def test_main_error(t):
		def mockSetLevel(level):
			raise ValueError(level)
		try:
			pydor.log.setLevel = mockSetLevel
			assert pydor.main(['--log', 'invalid']) == pydor.ErrorType['ArgsError'].value
		finally:
			del pydor.log
			pydor.log = MockLog()

class TestPydor(TestCase):

	def test_cmd(t):
		# test it with an error so it doesn't really runs
		def mockSetLevel(level):
			raise ValueError(level)
		try:
			pydor.log.setLevel = mockSetLevel
			rc = cmdrun(['python3', 'pydor.py', '--log', 'invalid'])
			assert rc == pydor.ErrorType['ArgsError'].value
		finally:
			del pydor.log
			pydor.log = MockLog()

# main

if __name__ == '__main__':
	main()
