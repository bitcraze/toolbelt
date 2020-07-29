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

__author__ = 'kristoffer'


class Git:
    def __init__(self, subproc):
        self.subproc = subproc

    def clone(self, repo, destination, tag=None, depth=None):
        params = ["git", "clone", '--recursive']

        if tag is not None:
            params.append('--branch=' + str(tag))

        if depth is not None:
            params.append('--depth=' + str(depth))

        params.append(repo)
        params.append(destination)

        self.subproc.check_call(params, stdout=self.subproc.devnull,
                                stderr=self.subproc.devnull)
