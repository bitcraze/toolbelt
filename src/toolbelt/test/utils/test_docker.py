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
import subprocess
import unittest
from unittest.mock import MagicMock, ANY, call, patch

from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException
from toolbelt.utils.subproc import SubProc


class DockerTest(unittest.TestCase):

    def setUp(self):
        self.sub_proc_mock = MagicMock(SubProc)

        self.sut = Docker(sub_proc=self.sub_proc_mock)

    def test_that_container_exists_returns_true_when_result_is_0(self):
        # Fixture
        name = "theName"
        self.sub_proc_mock.call.return_value = 0

        # Test
        actual = self.sut.container_exist(name)

        # Assert
        self.assertTrue(actual)
        self.sub_proc_mock.call.assert_called_once_with(
            ["docker", "inspect", "--format={{.Id}}", name],
            stdout=ANY, stderr=subprocess.STDOUT)

    def test_that_container_exists_returns_false_when_result_is_not_0(self):
        # Fixture
        name = "theName"
        self.sub_proc_mock.call.return_value = 1

        # Test
        actual = self.sut.container_exist(name)

        # Assert
        self.assertFalse(actual)

    def test_that_stop_and_remove_container_makes_the_right_calls(self):
        # Fixture
        name = "theName"
        expected_calls = [
            call(["docker", "stop", name], stdout=ANY),
            call(["docker", "rm", "-v", name], stdout=ANY)
        ]

        # Test
        self.sut.stop_and_remove_container(name)

        # Assert
        self.sub_proc_mock.check_call.assert_has_calls(expected_calls)

    def test_that_push_makes_the_right_calls(self):
        # Fixture
        name = "theName"

        # Test
        self.sut.push(name)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ["docker", "push", name])

    def test_that_image_exist_returns_true_when_no_exception_is_raised(self):
        # Fixture
        name = "theName"

        # Test
        actual = self.sut.image_exists(name)

        # Assert
        self.assertTrue(actual)
        self.sub_proc_mock.check_output.assert_called_once_with(
                ["docker", "pull", name], stderr=subprocess.STDOUT)

    def test_that_image_exist_returns_false_when_image_is_not_found(self):
        # Fixture
        name = "theName"
        self.sub_proc_mock.check_output.side_effect = ToolbeltException(
                'Error: image library/undefined not found')

        # Test
        actual = self.sut.image_exists(name)

        # Assert
        self.assertFalse(actual)

    def test_that_image_exist_returns_raises_exception(self):
        # Fixture
        name = "theName"
        self.sub_proc_mock.check_output.side_effect = ToolbeltException(
                'Other message')

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.image_exists(name)

    def test_run_in_container(self):
        # Fixture
        uid = '123'
        image_name = "anImage"
        args = ['a1', 'a2']
        volumes = [('v1', 'v2'), ('v3', 'v4')]
        volumes_from = ['vf1', 'vf2']

        with patch('sys.stdout') as mock:
            mock.isatty.return_value = True

            # Test
            self.sut.run_in_container(uid, image_name, args, volumes,
                                      volumes_from)

            # Assert
            self.sub_proc_mock.check_call.assert_called_once_with(
                    ['docker', 'run', '--rm', '-u', uid, '-v',
                     '/var/run/docker.sock:/var/run/docker.sock', '-it',
                     '-v', 'v1:v2', '-v', 'v3:v4',
                     '--volumes-from', 'vf1', '--volumes-from', 'vf2',
                     image_name, 'a1', 'a2'])

    def test_run_in_container_with_port(self):
        # Fixture
        uid = '123'
        image_name = "anImage"
        args = ['a1', 'a2']
        ports = [('80', '8080')]

        with patch('sys.stdout') as mock:
            mock.isatty.return_value = True

            # Test
            self.sut.run_in_container(uid, image_name, args, ports=ports)

            # Assert
            self.sub_proc_mock.check_call.assert_called_once_with(
                    ['docker', 'run', '--rm', '-u', uid, '-v',
                     '/var/run/docker.sock:/var/run/docker.sock', '-it',
                     '-p', '80:8080',
                     image_name, 'a1', 'a2'])

    def test_run_in_container_no_tty(self):
        # Fixture
        uid = '123'
        image_name = "anImage"
        args = []

        with patch('sys.stdout') as mock:
            mock.isatty.return_value = False

            # Test
            self.sut.run_in_container(uid, image_name, args)

            # Assert
            self.sub_proc_mock.check_call.assert_called_once_with(
                ['docker', 'run', '--rm', '-u', uid, '-v',
                 '/var/run/docker.sock:/var/run/docker.sock',
                 image_name])

    def test_run_script_in_container(self):
        # Fixture
        uid = '123'
        image_name = "anImage"
        script = 'doit.sh'
        script_args = ['a1', 'a2']
        volumes = [('v1', 'v2'), ('v3', 'v4')]
        volumes_from = ['vf1', 'vf2']

        with patch('sys.stdout') as mock:
            mock.isatty.return_value = True

            # Test
            self.sut.run_script_in_container(uid, image_name, script,
                                             script_args, volumes,
                                             volumes_from)

            # Assert
            self.sub_proc_mock.check_call.assert_called_once_with(
                    ['docker', 'run', '--rm', '-u', uid, '-v',
                     '/var/run/docker.sock:/var/run/docker.sock', '-it',
                     '-v', 'v1:v2', '-v', 'v3:v4',
                     '--volumes-from', 'vf1', '--volumes-from', 'vf2',
                     image_name, script, 'a1', 'a2'])

    def test_list_images(self):
        # Fixture
        out1 = "REPOSITORY                               TAG                 IMAGE ID            CREATED             SIZE\n"  # noqa
        out2 = "repo/image1                              49                  1b69f8ee3b87        7 hours ago         675.2 MB\n"  # noqa
        out3 = "repo/image2                              17                  bcf6d6f25607        12 hours ago        675.1 MB"  # noqa

        self.sub_proc_mock.check_output.return_value = out1 + out2 + out3

        expected = [
            {"repo": 'repo/image1', "tag": '49', "id": '1b69f8ee3b87'},
            {"repo": 'repo/image2', "tag": '17', "id": 'bcf6d6f25607'},
        ]

        # Test
        actual = self.sut.list_images()

        # Assert
        self.sub_proc_mock.check_output.assert_called_once_with(
                ['docker', 'images'])
        self.assertEqual(expected, actual)

    def test_remove_images(self):
        # Fixture
        images = ['i1', 'i2']

        # Test
        self.sut.remove_images(images)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ['docker', 'rmi', 'i1', 'i2'])

    def test_tag(self):
        # Fixture
        existing_image = "existing"
        new_image = "new"

        # Test
        self.sut.tag(existing_image, new_image)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ['docker', 'tag', existing_image, new_image])

    def test_pull(self):
        # Fixture
        image = "someImage"

        # Test
        self.sut.pull(image)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ['docker', 'pull', image])

    def test_inspect(self):
        # Fixture
        container = "my-container"
        expected = [{"Id": "123123", "Created": "2016-02-21T12:..."}]
        data = json.dumps(expected)
        self.sub_proc_mock.check_output.return_value = data

        # Test
        actual = self.sut.inspect(container)

        # Assert
        self.assertEqual(expected, actual)
        self.sub_proc_mock.check_output.assert_called_once_with(
                ["docker", "inspect", container])

    def test_list_volumes(self):
        # Fixture
        self.sub_proc_mock.check_output.return_value = "123\n456\n789"

        expected = [
            "123",
            "456",
            "789",
        ]

        # Test
        actual = self.sut.list_volumes()

        # Assert
        self.sub_proc_mock.check_output.assert_called_once_with(
            ['docker', 'volume', 'ls', '-q'])
        self.assertEqual(expected, actual)

    def test_list_volumes_with_filter(self):
        # Fixture
        self.sub_proc_mock.check_output.return_value = "123\n456\n789"

        expected = [
            "123",
            "456",
            "789",
        ]

        # Test
        actual = self.sut.list_volumes(filter='a_filter')

        # Assert
        self.sub_proc_mock.check_output.assert_called_once_with(
            ['docker', 'volume', 'ls', '-q', '-f', 'a_filter'])
        self.assertEqual(expected, actual)

    def test_remove_volumes(self):
        # Fixture
        ids = [
            "123",
            "456",
            "789",
        ]

        # Test
        self.sut.remove_volumes(ids)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
            ['docker', 'volume', 'rm', '123', '456', '789'])
