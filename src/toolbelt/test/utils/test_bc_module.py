# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
# Toolbelt - a utility tu run tools in docker containers
# Copyright (C) 2016  Bitcraze AB
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

import subprocess
import unittest
from unittest.mock import MagicMock, patch, mock_open

import json

from toolbelt.utils.bc_module import BcModule
from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException
from toolbelt.utils.file_wrapper import FileWrapper
from toolbelt.utils.runner import Runner


class BcModuleTest(unittest.TestCase):

    def setUp(self):
        self.docker_mock = MagicMock(Docker)
        self.runner_mock = MagicMock(Runner)
        self.file_wrapper_mock = MagicMock(FileWrapper)

        self.config = {"version": "1.0", "a": "b"}
        self.file_wrapper_mock.json_load.return_value = self.config

        self.sut = BcModule(self.docker_mock, self.runner_mock,
                            self.file_wrapper_mock)

    def test_read_config_reads_config(self):
        # Fixture
        path = "/module/root"

        # Test
        actual = self.sut.read_config(path)

        # Assert
        self.assertEqual("b", actual['a'])
        self.file_wrapper_mock.json_load.assert_called_once_with(
                path + '/module.json')

    def test_read_config_reads_raises_exception_on_missing_version(self):
        # Fixture
        self.file_wrapper_mock.json_load.return_value = {}

        # Assert
        with self.assertRaises(ToolbeltException):

            # Test
            self.sut.read_config("/module/root")

    def test_execute_tool(self):
        # Fixture
        path_to_root = 'pathToRoot'
        module_root_in_docker_host = "moduleRootInDockerHost"
        module_config = {"version": "1.0", "a": "b"}
        tb_config = {'module_root': path_to_root,
                     'module_root_in_docker_host': module_root_in_docker_host}
        command = 'cmd'
        arguments = ['a1']

        self.file_wrapper_mock.json_load.return_value = module_config

        # Test
        self.sut.execute_tool(tb_config, command, arguments)

        # Assert
        self.runner_mock.run_script_in_env.assert_called_once_with(
                tb_config, module_config, 'tools/build/' + command,
                module_root_in_docker_host, arguments)

    def test_enumerate_tools(self):
        # Fixture
        with patch('os.listdir') as mock:
            module_root = "moduleRoot"
            expected = ['result']
            mock.return_value = expected

            # Test
            actual = self.sut.enumerate_tools(module_root)

            # Assert
            self.assertEqual(expected, actual)
            mock.assert_called_once_with(module_root + "/tools/build")

    def test_enumerate_tools_nothing_found(self):
        # Fixture
        with patch('os.listdir') as mock:
            module_root = "moduleRoot"
            mock.side_effect = OSError()

            # Test
            actual = self.sut.enumerate_tools(module_root)

            # Assert
            self.assertEqual([], actual)

    def test_verify_config_version_returns_on_OK_version(self):
        # Fixture

        # Test
        self.sut.verify_config_version({'version': '1.0'})

        # Assert

    def test_verify_config_version_raises_exception_on_missing_version(self):
        # Fixture

        # Assert
        with self.assertRaises(ToolbeltException):

            # Test
            self.sut.verify_config_version({})

    def test_verify_config_version_raises_exception_on_wrong_version(self):
        # Fixture

        # Assert
        with self.assertRaises(ToolbeltException):

            # Test
            self.sut.verify_config_version({'version': '2.0'})
