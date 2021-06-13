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
from unittest.mock import MagicMock, call

from toolbelt.belt.version import Version
from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException


class VersionTest(unittest.TestCase):

    def setUp(self):
        self.tb_config = {'container_id': 'my-container', 'host': 'container'}
        self.docker_mock = MagicMock(spec=Docker)

        self.sut = Version(docker=self.docker_mock)

    def test_that_we_get_error_for_too_many_arguments(self):
        # Fixture
        args = ["a"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_version(self):
        # Fixture
        image_id = "4711"
        image_name = "my/image:latest"
        self.docker_mock.inspect.side_effect = [
            [{"Image": image_id, "Config": {"Image": image_name}}],
            [{'Created': "2016-01-01..."}]]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_has_calls([
            call('my-container'),
            call(image_id)])
