# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from contextlib import contextmanager
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

# helper funcs

def _envDir(env, *parts):
	d = path.join(_srcdir, 'testdata', env.replace('/', path.sep))
	if len(parts) > 0:
		d = path.join(d, *parts)
	return d

# testing config

@contextmanager
def _envConfig(env, filename):
	fn = _envDir(env, filename)
	try:
		del pydor.config
		pydor.config = pydor.Config()
		pydor.config.read(filename = fn)
		yield pydor.config
	finally:
		del pydor.config
		pydor.config = pydor.Config()

# testing env

@contextmanager
def env(name, cfgfn = 'pydor.ini'):
	envdir = _envDir(name)
	try:
		chdir(envdir)
		with _envConfig(name, cfgfn) as cfg:
			yield cfg
	finally:
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

	def test_default(t):
		with env('config', 'nofile.ini') as cfg:
			assert isinstance(cfg, pydor.Config)
			assert isinstance(cfg._cfg, ConfigParser)
			assert cfg._cfg.defaults() == {
				'requirements': 'requirements.txt',
			}
			assert cfg._cfg.sections() == []
			assert cfg._readFiles == []
			assert not cfg._cfg.has_section('pydor')

	def test_read(t):
		with env('config') as cfg:
			assert cfg._readFiles[0].endswith('pydor.ini')
			assert cfg._cfg.has_section('pydor')

	def test_other_files(t):
		with env('config.other_files', 'setup.cfg') as cfg:
			assert cfg._readFiles[0].endswith('setup.cfg')
			assert cfg._cfg.has_section('pydor')

# test pydor commands

class TestMain(TestCase):

	def test_main(t):
		with env('cmd/main'):
			assert pydor.main([]) == 0

	def test_main_error(t):
		def mockSetLevel(level):
			raise ValueError(level)
		try:
			pydor.log.setLevel = mockSetLevel
			assert pydor.main(['--log', 'testing']) == pydor.ErrorType['ArgsError'].value
		finally:
			del pydor.log
			pydor.log = MockLog()

class TestPydor(TestCase):

	def test_cmd(t):
		# test it with an error so it doesn't really runs
		rc = cmdrun(['python3', 'pydor.py', '--log', 'testing'])
		assert rc == pydor.ErrorType['ArgsError'].value

# main

if __name__ == '__main__':
	main()
