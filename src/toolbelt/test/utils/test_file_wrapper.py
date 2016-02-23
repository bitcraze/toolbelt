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

import json
import unittest
from unittest.mock import patch, mock_open

from toolbelt.utils.file_wrapper import FileWrapper


class FileWrapperTest(unittest.TestCase):

    def setUp(self):
        self.sut = FileWrapper()

    def test_json_load(self):
        # Fixture
        path = "some/path"
        data = {'some': 'data'}
        data_json = json.dumps(data)

        with patch('builtins.open', mock_open(read_data=data_json),
                   create=True) as mock:

            # Test
            actual = self.sut.json_load(path)

            # Assert
            self.assertEqual(data, actual)
            mock.assert_called_once_with(path, 'r')

    def test_json_dump(self):
        # Fixture
        path = "some/path"
        data = {'some': 'data'}
        data_json = json.dumps(data)

        with patch('builtins.open', mock_open(read_data=data_json),
                   create=True) as mock:

            # Test
            self.sut.json_dump(data, path)

            # Assert
            mock.assert_called_once_with(path, 'w')

    def test_read(self):
        # Fixture
        path = "some/path"
        data = 'Some data'

        with patch('builtins.open', mock_open(read_data=data),
                   create=True) as mock:

            # Test
            actual = self.sut.read(path)

            # Assert
            self.assertEqual(data, actual)
            mock.assert_called_once_with(path, 'r')
