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

import os
import unittest
from unittest.mock import patch, MagicMock, call

from toolbelt.utils.bc_module import BcModule
from toolbelt.utils.config_reader import ConfigReader
from toolbelt.utils.file_wrapper import FileWrapper


class RunnerTest(unittest.TestCase):

    ROOT_UID = "0"

    FULL_CONFIG = {'CALLING_UID': "123",
                   'CALLING_OS': 'Linux'}

    def setUp(self):
        self.file_wrapper_mock = MagicMock(FileWrapper)
        self.bc_module_mock = MagicMock(BcModule)

        self.default_config = {'some': 'data'}
        self.file_wrapper_mock.json_load.side_effect = [
            self.default_config, IOError()]

        self.bc_module_mock.enumerate_tools.return_value = []

        self.extensions_mock = MagicMock()
        self.extensions_mock.tools.return_value = []

        self.toolbelt_root = 'path'

        self.mock_tools = ['dummy1', 'dummy2']

        self.sut = ConfigReader(file_wrapper=self.file_wrapper_mock,
                                bc_module=self.bc_module_mock,
                                tools=self.mock_tools)

    def test_read_tb_config(self):
        # Fixture

        # Test
        actual = self.sut.get_tb_config(self.toolbelt_root,
                                        self.extensions_mock)

        # Assert
        self.assertEqual("data", actual['some'])
        self.file_wrapper_mock.json_load.assert_has_calls([
            call(self.toolbelt_root + '/config.json'),
            call(self.toolbelt_root + '/.toolbelt.json')])

    def test_read_tb_config_data_merged(self):
        # Fixture
        self.file_wrapper_mock.json_load.side_effect = [
            {'some': 'data'},
            {'more': 'info'}
        ]

        # Test
        actual = self.sut.get_tb_config(self.toolbelt_root,
                                        self.extensions_mock)

        # Assert
        self.assertEqual("data", actual['some'])
        self.assertEqual("info", actual['more'])

    def test_read_tb_config_data_replaced(self):
        # Fixture
        self.file_wrapper_mock.json_load.side_effect = [
            {'some': 'data'},
            {'some': 'info'}
        ]

        # Test
        actual = self.sut.get_tb_config(self.toolbelt_root,
                                        self.extensions_mock)

        # Assert
        self.assertEqual("info", actual['some'])

    def test_paths(self):
        # Fixture
        currentDir = os.getcwd()

        # Test
        actual = self.sut.get_tb_config(self.toolbelt_root,
                                        self.extensions_mock)

        # Assert
        self.assertEqual(self.toolbelt_root, actual['root'])
        self.assertEqual(self.toolbelt_root + "/tmp", actual['tmpRoot'])
        self.assertEqual(currentDir, actual['module_root'])
        self.assertEqual(currentDir, actual['module_root_in_docker_host'])

    def test_nr_of_module_tools_for_current_directory(self):
        with patch.dict('os.environ', self.FULL_CONFIG):
            # Fixture

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual([], actual['module_tools'])

    def test_nr_of_registered_tools(self):
        # Fixture

        # Test
        actual = self.sut.get_tb_config(self.toolbelt_root,
                                        self.extensions_mock)

        # Assert
        self.assertEqual(len(self.mock_tools), len(actual['tools']))

    def test_config_set_by_code_in_container_env(self):
        # Fixture
        path = "some/path"
        container_id = "someId"

        with patch.dict('os.environ', {'HOST_CW_DIR': path,
                                       "HOSTNAME": container_id}):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(path, actual['module_root_in_docker_host'])
            self.assertEqual(container_id, actual['container_id'])

    def test_config_set_by_uid(self):
        # Fixture
        with patch.dict('os.environ', {'CALLING_UID': "123",
                                       'CALLING_OS': 'Linux'}):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual("123", actual['uid'])

    def test_config_root_when_uid_is_missing(self):
        # Fixture
        with patch.dict('os.environ'):
            os.environ['CALLING_OS'] = 'Linux'
            if 'CALLING_UID' in os.environ:
                os.environ.pop('CALLING_UID')

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(self.ROOT_UID, actual['uid'])

    def test_config_root_uid_when_empty(self):
        # Fixture
        with patch.dict('os.environ', {'CALLING_UID': "",
                                       'CALLING_OS': 'Linux'}):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(self.ROOT_UID, actual['uid'])

    def test_config_root_uid_when_no_os(self):
        # Fixture
        with patch.dict('os.environ', {'CALLING_UID': "123"}):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(self.ROOT_UID, actual['uid'])

    def test_config_root_uid_when_not_linux(self):
        # Fixture
        with patch.dict('os.environ', {'CALLING_UID': "123",
                                       'CALLING_OS': 'Darwin'}):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(self.ROOT_UID, actual['uid'])

    def test_module_tools_added(self):
        with patch.dict('os.environ', self.FULL_CONFIG):
            # Fixture
            expected = {"build": ["nr1", "nr2"], "build-docs": ["nr3"]}
            self.bc_module_mock.enumerate_tools.return_value = expected

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(expected, actual['module_tools'])

    def test_module_config_added(self):
        # Fixture
        with patch.dict('os.environ', self.FULL_CONFIG):
            expected = {"some": "config"}
            self.bc_module_mock.read_config.return_value = expected

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertEqual(expected, actual['module_config'])

    def test_config_ok_flag_is_set(self):
        # Fixture
        with patch.dict('os.environ', self.FULL_CONFIG):

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertTrue(actual['config_ok'])

    def test_config_not_ok_without_os(self):
        # Fixture
        with patch.dict('os.environ', self.FULL_CONFIG):
            os.environ.pop('CALLING_OS')

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertFalse(actual['config_ok'])

    def test_config_not_ok_without_uid(self):
        # Fixture
        with patch.dict('os.environ', self.FULL_CONFIG):
            os.environ.pop('CALLING_UID')

            # Test
            actual = self.sut.get_tb_config(self.toolbelt_root,
                                            self.extensions_mock)

            # Assert
            self.assertFalse(actual['config_ok'])
