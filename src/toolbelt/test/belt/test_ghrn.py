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
import urllib
from unittest.mock import MagicMock, patch

from toolbelt.belt.ghrn import Ghrn
from toolbelt.utils.docker import Docker
from toolbelt.utils.exception import ToolbeltException


class GhrnTest(unittest.TestCase):
    def setUp(self):
        self.tb_config = {'container_id': 'my-container', 'host': 'container'}
        self.docker_mock = MagicMock(spec=Docker)

        self.milestones = [
            {"title": "Title 1", "number": 1},
            {"title": "Title 2", "number": 2},
        ]

        self.sut = Ghrn(docker=self.docker_mock)

    def test_that_we_get_error_for_too_many_arguments(self):
        # Fixture
        args = ["a", "b", "c"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_that_we_get_error_for_too_few_arguments(self):
        # Fixture
        args = ["a"]

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut.command(self.tb_config, args)

    def test_find_existing_milestone_id(self):
        # Fixture

        # Test
        actual = self.sut._find_milestone_id(self.milestones, "Title 2")

        # Assert
        expected = 2
        self.assertEqual(expected, actual)

    def test_find_non_existing_milestone_id(self):
        # Fixture

        # Test
        # Assert
        with self.assertRaises(ToolbeltException):
            self.sut._find_milestone_id(self.milestones, "Not existing")

    def test_collect_issues(self):
        # Fixture
        issues = [
            {
                "number": 4711,
                "title": "Problem"
            },
            {
                "number": 17,
                "title": "Some issue"
            },
        ]

        # Test
        actual = self.sut._collect_issues(issues)

        # Assert
        expected = "#17 Some issue\n#4711 Problem\n"
        self.assertEqual(expected, actual)

    def test_api_get_no_pagination(self):
        # Fixture
        with patch('urllib.request.urlopen') as mock:
            mock.return_value.read.return_value = b'[{"some":"json"}]'

            # Test
            actual = self.sut._api_get("the/url/to/test")

            # Assert
            expected = [{"some": "json"}]
            self.assertEqual(expected, actual)

    def test_api_get_404(self):
        # Fixture
        with self.assertRaises(ToolbeltException):
            with patch('urllib.request.urlopen') as mock:
                mock.side_effect = urllib.error.HTTPError("the/url", 404,
                                                          "oups!", None, None)

                # Test
                # Assert
                self.sut._api_get("non/existing/url")

    def test_api_get_with_pagination(self):
        # Fixture
        with patch('urllib.request.urlopen') as mock:
            instance = mock.return_value
            instance.read.side_effect = [b'[{"part":"1"}]', b'[{"part":"2"}]']
            instance.getheader.side_effect = [
                '<the/url/to/test?page=2>; rel="next", <the/url/to/test?page=2>; rel="last"',  # noqa
                None]

            # Test
            actual = self.sut._api_get("the/url/to/test")

            # Assert
            expected = [{"part": "1"}, {"part": "2"}]
            self.assertEqual(expected, actual)
