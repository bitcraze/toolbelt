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
from unittest.mock import MagicMock, ANY

from toolbelt.utils.git import Git
from toolbelt.utils.subproc import SubProc


class GitTest(unittest.TestCase):

    def setUp(self):
        self.sub_proc_mock = MagicMock(SubProc)

        self.sut = Git(self.sub_proc_mock)

    def test_clone(self):
        # Fixture
        repo = "aRepo"
        destination = "path"

        # Test
        self.sut.clone(repo, destination)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ["git", "clone", '--recursive', repo, destination],
                stdout=ANY, stderr=ANY)

    def test_clone_all_params(self):
        # Fixture
        repo = "aRepo"
        destination = "path"
        tag = "aTag"
        depth = 17

        # Test
        self.sut.clone(repo, destination, tag, depth)

        # Assert
        self.sub_proc_mock.check_call.assert_called_once_with(
                ["git", "clone", '--recursive', '--branch=' + tag,
                 '--depth=' + str(depth), repo, destination],
                stdout=ANY, stderr=ANY)
