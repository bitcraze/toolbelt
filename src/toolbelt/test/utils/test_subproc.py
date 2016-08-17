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
from unittest.mock import MagicMock

from toolbelt.utils.subproc import SubProc
from toolbelt.utils.exception import ToolbeltException


class SubprocTest(unittest.TestCase):

    def setUp(self):
        self.sut = SubProc()

    def test_that_call_passes_args_on(self):
        # Fixture
        subprocess.call = MagicMock(return_value=47)

        # Test
        actual = self.sut.call(1, "string", name="value")

        # Assert
        subprocess.call.assert_called_with(1, "string", name="value")
        self.assertEqual(47, actual)

    def test_that_call_handles_exception(self):
        # Fixture
        subprocess.call = MagicMock(
                side_effect=subprocess.CalledProcessError(
                        17, 'cmd', b'output'))

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.call()

    def test_that_check_call_passes_args_on(self):
        # Fixture
        subprocess.check_call = MagicMock(return_value=b'Some string')

        # Test
        self.sut.check_call(1, "string", name="value")

        # Assert
        subprocess.check_call.assert_called_with(1, "string", name="value")

    def test_that_check_call_handles_exception(self):
        # Fixture
        subprocess.check_call = MagicMock(
                side_effect=subprocess.CalledProcessError(
                        17, 'message', b'output'))

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.check_call()

    def test_that_check_output_passes_args_on(self):
        # Fixture
        subprocess.check_output = MagicMock(return_value=b'Some string')

        # Test
        self.sut.check_output(1, "string", name="value")

        # Assert
        subprocess.check_output.assert_called_with(1, "string", name="value")

    def test_that_check_output_handles_exception(self):
        # Fixture
        subprocess.check_output = MagicMock(
                side_effect=subprocess.CalledProcessError(
                        17, 'message', b'output'))

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.check_output()

    def test_that_output_is_converted_to_utf8(self):
        # Fixture
        subprocess.check_output = MagicMock(return_value=b'Some string')

        # Test
        actual = self.sut.check_output()

        # Assert
        self.assertEqual('Some string', actual)
