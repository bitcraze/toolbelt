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

from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException
from toolbelt.utils.runner import Runner


class RunnerTest(unittest.TestCase):

    def setUp(self):
        self.docker_mock = MagicMock(Docker)

        self.sut = Runner(docker=self.docker_mock)

    def test_run_script_in_env(self):
        # Fixture
        module_config = {'environmentReqs': {'build': ['theReq']}}
        tb_config = {'environments': {'imageName': ['theReq']}, 'uid': '123', 'module_config': module_config}
        module_root_in_docker_host = "path"
        script = "tools/build/script"
        script_args = ['a', 'b']

        # Test
        self.sut.run_script_in_env(tb_config, script,
                                   module_root_in_docker_host, script_args)

        # Assert
        self.docker_mock.run_script_in_container.assert_called_once_with(
                '123', 'imageName', script, script_args,
                volumes=[(module_root_in_docker_host, '/module')])

    def test_run_script_in_env_no_env_found_should_raise(self):
        # Fixture
        module_config = {'environmentReqs': {'build': ['unmatched_req']}}
        tb_config = {'environments': {'imageName': ['theReq']}, 'module_config': module_config}
        module_root_in_docker_host = "path"
        script = "tools/build/script"
        script_args = []

        # Assert
        with self.assertRaises(ToolbeltException):

            # Test
            self.sut.run_script_in_env(tb_config, script,
                                       module_root_in_docker_host, script_args)

    def test_use_matching_env(self):
        # Fixture
        module_config = {'environmentReqs': {'build': ['req1', 'req2']}}
        tb_config = {'environments': {'imageName': ['req1', 'req2'],
                                      'wrongImage': ['req1']},
                     'uid': '123',
                     'module_config': module_config}
        module_root_in_docker_host = "path"
        script = "tools/build/script"
        script_args = ['a', 'b']

        # Test
        self.sut.run_script_in_env(tb_config, script,
                                   module_root_in_docker_host, script_args)

        # Assert
        self.docker_mock.run_script_in_container.assert_called_once_with(
                '123', 'imageName', script, script_args,
                volumes=[(module_root_in_docker_host, '/module')])
