# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
# Toolbelt - a utility tu run tools in docker containers
# Copyright (C) 2019  Bitcraze AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import MagicMock

from toolbelt.belt.docs import Docs
from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException


class DocsTest(unittest.TestCase):

    def setUp(self):
        self.tb_config = {'uid': 'a-uid',
                          'module_root_in_docker_host': '/some/path'}
        self.docker_mock = MagicMock(spec=Docker)

        self.image_name = 'bitcraze/web-builder'
        self.default_args = ['jekyll', 'serve', '--host', '0.0.0.0',
                             '--incremental', '--config',
                             '/docs-config.yml']
        self.default_args_jekyll_port = ['--port', '80']
        self.expected_volumes = [('/some/path/docs', '/module/docs')]

        self.sut = Docs(docker=self.docker_mock)

    def test_that_we_get_error_for_too_many_arguments(self):
        # Fixture
        args = ["80", "12"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_that_we_get_error_if_port_is_not_an_integer(self):
        # Fixture
        args = ["a_string"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_docs_without_port(self):
        # Fixture

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.run_in_container.assert_called_once_with(
            'a-uid',
            'bitcraze/web-builder',
            self.default_args + self.default_args_jekyll_port,
            self.expected_volumes, ports=[('80', '80')])

    def test_docs_with_port(self):
        # Fixture

        # Test
        self.sut.command(self.tb_config, ['8080'])

        # Assert
        self.docker_mock.run_in_container.assert_called_once_with(
            'a-uid',
            'bitcraze/web-builder',
            self.default_args + ['--port', '8080'],
            self.expected_volumes, ports=[('8080', '8080')])
