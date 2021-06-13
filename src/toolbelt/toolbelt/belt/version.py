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

from toolbelt.utils.exception import ToolbeltException

__author__ = 'kristoffer'


class Version:
    names = ['version', '-V', '--version']
    short_description = "Display version of the tool belt"

    def __init__(self, docker):
        self._docker = docker

    def command(self, tb_config, arguments):
        if len(arguments) != 0:
            raise ToolbeltException("Not expecting any arguments")
        self._display_version(tb_config)

    def help(self):
        print("Usage:  tb version")
        print("Display the version of the tool belt. The version is the ")
        print("name of the current container + the creation date of the ")
        print("docker image that the current container is based on")

    def _display_version(self, tb_config):
        container = tb_config['container_id']
        container_data = self._docker.inspect(container)
        image_id = container_data[0]['Image']
        image_name = container_data[0]['Config']['Image']

        created = self._docker.inspect(image_id)[0]['Created']
        print(image_name + ' - ' + created)
