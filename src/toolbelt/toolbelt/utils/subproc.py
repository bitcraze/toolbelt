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
import subprocess

from toolbelt.utils import exception


class SubProc:
    devnull = ''

    def __init__(self):
        self.devnull = open(os.devnull, 'w')

    def __del__(self):
        self.devnull.close()

    def call(self, *popenargs, **kwargs):
        try:
            return subprocess.call(*popenargs, **kwargs)
        except subprocess.CalledProcessError as e:
            message = "The call '" + " ".join(e.cmd) + \
                      "' failed with error code " + str(e.returncode)
            if e.output:
                message += ", and output '" + e.output.decode('cp437') + "'"
            raise exception.ToolbeltException(message)

    def check_call(self, *popenargs, **kwargs):
        try:
            return subprocess.check_call(*popenargs, **kwargs)
        except subprocess.CalledProcessError as e:
            message = "The call '" + " ".join(e.cmd) + \
                      "' failed with error code " + str(e.returncode)
            if e.output:
                message += ", and output '" + e.output.decode('cp437') + "'"
            raise exception.ToolbeltException(message)

    def check_output(self, *popenargs, **kwargs):
        try:
            return subprocess.check_output(*popenargs, **kwargs).\
                decode('cp437')
        except subprocess.CalledProcessError as e:
            message = "The call '" + " ".join(e.cmd) + \
                      "' failed with error code " + str(e.returncode)
            if e.output:
                message += ", and output '" + e.output.decode('cp437') + "'"
            raise exception.ToolbeltException(message)
