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
from unittest.mock import MagicMock

from toolbelt.belt.update import Update
from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException


class UpdateTest(unittest.TestCase):

    def setUp(self):
        self.tb_config = {'container_id': 'my-container', 'host': 'container'}
        self.docker_mock = MagicMock(spec=Docker)

        self.sut = Update(docker=self.docker_mock)

    def test_that_we_get_error_for_too_many_arguments(self):
        # Fixture
        args = ["a"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_update(self):
        # Fixture
        self.docker_mock.inspect.return_value = [
            {"Config": {"Image": "some.registry:5000/toolbelt:11"}}]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_called_once_with('my-container')
        self.docker_mock.pull('some.registry:5000/toolbelt')

    def test_update_image_name_without_tag(self):
        # Fixture
        self.docker_mock.inspect.return_value = [
            {"Config": {"Image": "some.registry:5000/toolbelt"}}]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_called_once_with('my-container')
        self.docker_mock.pull.assert_called_once_with(
                'some.registry:5000/toolbelt')

    def test_update_image_name_without_registry(self):
        # Fixture
        self.docker_mock.inspect.return_value = [
            {"Config": {"Image": "toolbelt"}}]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_called_once_with('my-container')
        self.docker_mock.pull.assert_called_once_with('toolbelt')

    def test_update_image_name_with_registry_no_port(self):
        # Fixture
        self.docker_mock.inspect.return_value = [
            {"Config": {"Image": "registry/toolbelt"}}]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_called_once_with('my-container')
        self.docker_mock.pull.assert_called_once_with('registry/toolbelt')

    def test_update_image_name_without_registry_with_tag(self):
        # Fixture
        self.docker_mock.inspect.return_value = [
            {"Config": {"Image": "toolbelt:11"}}]

        # Test
        self.sut.command(self.tb_config, [])

        # Assert
        self.docker_mock.inspect.assert_called_once_with('my-container')
        self.docker_mock.pull.assert_called_once_with('toolbelt')
