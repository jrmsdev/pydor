# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from contextlib import contextmanager
from os import getcwd, path, chdir, devnull
from subprocess import call as cmdrun
from sys import executable as pyexe
from unittest import TestCase, main
from unittest.mock import Mock

import logging
import pydor
import pytest

_srcdir = path.abspath(getcwd())

# mock pydor.log

class MockLog(object):

	def setLevel(self, level):
		pass

	def error(self, msg, *args):
		pass

	def debug(self, msg, *args):
		pass

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
		del pydor.log
		pydor.log = MockLog()
		with _envConfig(name, cfgfn) as cfg:
			yield cfg
	finally:
		chdir(_srcdir)
		del pydor.log
		pydor.log = MockLog()

# test errors management

class TestError(TestCase):

	def test_default(t):
		err = pydor.Error('ArgsError', 'testing')
		assert err._typ == 'ArgsError'
		assert err.status == 10
		assert err.status == pydor.ErrorType.ArgsError.value
		assert str(err) == 'ArgsError: testing'

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
			assert pydor.main(['--log', 'critical']) == 1

	def test_main_error(t):
		with env('cmd/main'):
			rc = pydor.main(['--log', 'testing', 'proxy'])
			assert rc == pydor.ErrorType['ArgsError'].value

	def test_log_debug(t):
		args = Mock()
		args.log = 'debug'
		log = pydor._logInit(args)
		assert log.isEnabledFor(logging.DEBUG)

class TestPydor(TestCase):

	def test_cmd(t):
		# test source file is executable
		# test it with an error so it doesn't really runs
		cmd = f"{pyexe} pydor.py testing >{devnull} 2>{devnull}"
		rc = cmdrun(cmd, shell = True)
		assert rc == 2

# test proxy manager

class TestProxy(TestCase):

	def test_main(t):
		with env('cmd/proxy'):
			try:
				orig_wapp = pydor.proxy._wapp
				pydor.proxy._wapp = Mock()
				pydor.proxy._wapp.run = Mock()
				rc = pydor.main(['proxy'])
				assert rc == 0
			finally:
				del pydor.proxy._wapp
				pydor.proxy._wapp = orig_wapp

# test main

if __name__ == '__main__':
	main()
