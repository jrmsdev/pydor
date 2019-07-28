# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from unittest import TestCase, main

import pydor

class TestPydor(TestCase):

	def test_fake(t):
		assert True

class TestConfig(TestCase):

	def test_default(t):
		assert isinstance(pydor.config, pydor._Config)
		assert isinstance(pydor.config._cfg, ConfigParser)
		assert pydor.config._cfg.defaults() == {
			'requirements': 'requirements.txt',
		}
		assert pydor.config._cfg.sections() == []

if __name__ == '__main__':
	main()
