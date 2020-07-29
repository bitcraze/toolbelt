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


class Update:
    def __init__(self, docker):
        self._docker = docker

    names = ['update']
    short_description = "Update tool belt to latest version"

    def command(self, tb_config, arguments):
        if len(arguments) != 0:
            raise ToolbeltException("Not expecting any arguments")
        self._update(tb_config)

    def help(self):
        print("Usage:  tb update")
        print("Update the tool belt to the latest version")

    def _update(self, tb_config):
        container = tb_config['container_id']
        container_data = self._docker.inspect(container)
        image_name_with_tag = container_data[0]['Config']['Image']
        image_name = self.remove_tag(image_name_with_tag)

        print("Pulling " + image_name + ":latest")
        self._docker.pull(image_name)

    def remove_tag(self, image_name_with_tag):
        reg_sep_pos = image_name_with_tag.find('/')
        if reg_sep_pos == -1:
            reg_sep_pos = 0
        tag_sep_pos = image_name_with_tag.find(':', reg_sep_pos)

        if tag_sep_pos == -1:
            return image_name_with_tag
        else:
            return image_name_with_tag[:tag_sep_pos]
