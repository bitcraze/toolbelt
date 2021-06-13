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

import unittest
from unittest.mock import MagicMock, patch

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

        self.config = {"version": "2.0", "environmentReqs": ["b"]}
        self.file_wrapper_mock.json_load.return_value = self.config

        self.sut = BcModule(self.docker_mock, self.runner_mock,
                            self.file_wrapper_mock)

    def test_read_config_reads_config(self):
        # Fixture
        path = "/module/root"

        # Test
        actual = self.sut.read_config(path)

        # Assert
        self.assertEqual(["b"], actual['environmentReqs'])
        self.file_wrapper_mock.json_load.assert_called_once_with(
            path + '/module.json')

    def test_read_config_reads_v1_config_and_converts(self):
        # Fixture
        module_config = {"version": "1.0", "environmentReq": ["arm-none-eabi"]}
        self.file_wrapper_mock.json_load.return_value = module_config
        path = "/module/root"

        # Test
        actual = self.sut.read_config(path)

        # Assert
        expected = {"build": ["arm-none-eabi"]}
        self.assertEqual(expected, actual['environmentReqs'])

    def test_read_config_reads_v2(self):
        # Fixture
        expected = {"build": ["arm-none-eabi"], "build-dox": ["doxygen"]}
        module_config = {"version": "2.0", "environmentReqs": expected}
        self.file_wrapper_mock.json_load.return_value = module_config
        path = "/module/root"

        # Test
        actual = self.sut.read_config(path)

        # Assert
        self.assertEqual(expected, actual['environmentReqs'])

    def test_read_config_reads_raises_exception_on_missing_version(self):
        # Fixture
        self.file_wrapper_mock.json_load.return_value = {}

        # Assert
        with self.assertRaises(ToolbeltException):
            # Test
            self.sut.read_config("/module/root")

    def test_execute_tool(self):
        # Fixture
        command = 'cmd'
        dir = 'build'
        path_to_root = 'pathToRoot'
        module_root_in_docker_host = "moduleRootInDockerHost"
        tb_config = {'module_root': path_to_root,
                     'module_root_in_docker_host': module_root_in_docker_host,
                     'module_tools': {command: dir}}
        arguments = ['a1']

        # Test
        self.sut.execute_tool(tb_config, command, arguments)

        # Assert
        self.runner_mock.run_script_in_env.assert_called_once_with(
            tb_config, 'tools/' + dir + '/' + command,
            module_root_in_docker_host, arguments)

    def test_enumerate_tools(self):
        # Fixture
        dir1 = "build"
        dir2 = "build-docs"
        tool1 = "tool1"
        tool2 = "tool2"
        tool3 = "tool3"

        def side_effect(*args, **kwargs):
            if args[0] == module_root + "/tools/" + dir1:
                return [tool1, tool2]
            if args[0] == module_root + "/tools/" + dir2:
                return [tool3]
            raise "Should not get here"

        with patch('os.listdir') as mock:
            module_root = "moduleRoot"
            mock.side_effect = side_effect
            module_config = {"environmentReqs": {dir1: ["bla"], dir2: ["ha"]}}
            expected = {tool1: dir1, tool2: dir1, tool3: dir2}

            # Test
            actual = self.sut.enumerate_tools(module_root, module_config)

            # Assert
            self.assertEqual(expected, actual)

    def test_enumerate_tools_nothing_found(self):
        # Fixture
        dir1 = "build"
        dir2 = "build-docs"
        tool3 = "tool3"

        def side_effect(*args, **kwargs):
            if args[0] == module_root + "/tools/" + dir1:
                raise OSError()
            if args[0] == module_root + "/tools/" + dir2:
                return [tool3]
            raise "Should not get here"

        with patch('os.listdir') as mock:
            module_root = "moduleRoot"
            mock.side_effect = side_effect
            module_config = {"environmentReqs": {dir1: ["bla"], dir2: ["ha"]}}
            expected = {tool3: dir2}

            # Test
            actual = self.sut.enumerate_tools(module_root, module_config)

            # Assert
            self.assertEqual(expected, actual)

    def test_that_duplication_of_tool_name_raises_exception(self):
        # Fixture
        dir1 = "build"
        dir2 = "build-docs"
        tool = "same-name"

        def side_effect(*args, **kwargs):
            if args[0] == module_root + "/tools/" + dir1:
                return [tool]
            if args[0] == module_root + "/tools/" + dir2:
                return [tool]
            raise "Should not get here"

        with patch('os.listdir') as mock:
            module_root = "moduleRoot"
            mock.side_effect = side_effect
            module_config = {"environmentReqs": {dir1: ["bla"], dir2: ["ha"]}}

            # Assert
            with self.assertRaises(ToolbeltException):
                # Test
                self.sut.enumerate_tools(module_root, module_config)

    def test_verify_config_version_returns_on_version_1(self):
        # Fixture

        # Test
        self.sut.verify_config_version({'version': '1.0'})

        # Assert

    def test_verify_config_version_returns_on_version_2(self):
        # Fixture

        # Test
        self.sut.verify_config_version({'version': '2.0'})

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
            self.sut.verify_config_version({'version': '3.0'})
