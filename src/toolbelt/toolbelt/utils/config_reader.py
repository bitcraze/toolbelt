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

from toolbelt.belt import help
from toolbelt.belt import update
from toolbelt.belt import version
from toolbelt.utils.bc_module import BcModule
from toolbelt.utils.file_wrapper import FileWrapper

__author__ = 'kristoffer'


class ConfigReader:
    CONFIG_FILE = 'config.json'
    PRIVATE_CONFIG_FILE = '.toolbelt.json'

    def __init__(self, file_wrapper=FileWrapper(), bc_module=BcModule()):
        self.file_wrapper = file_wrapper
        self.bc_module = bc_module

    def get_tb_config(self, toolbelt_root, extensions):
        tb_config = self._read_tb_config(toolbelt_root)

        # Path to the toolbelt in local file system
        tb_config['root'] = toolbelt_root

        # On OSX we must use a tmp dir in the users file tree since docker only
        # can access files here.
        tb_config['tmpRoot'] = toolbelt_root + "/tmp"

        tb_config['tools'] = self._register_tools(extensions)

        # Path to module root in local file system
        tb_config['module_root'] = os.getcwd()

        # Path to module root in docker host file system
        tb_config['module_root_in_docker_host'] = tb_config['module_root']

        # Is the toolbelt is running in native environment or a docker
        # container
        tb_config['host'] = 'native'

        if "HOST_CW_DIR" in os.environ:
            tb_config['module_root_in_docker_host'] = os.environ["HOST_CW_DIR"]
            tb_config['host'] = 'container'
            tb_config['container_id'] = os.environ["HOSTNAME"]

        tb_config['module_tools'] = \
            self.bc_module.enumerate_tools(tb_config['module_root'])

        return tb_config

    def _register_tools(self, extensions):
        return [
                   help.Help(),
                   update.Update(),
                   version.Version()
               ] + extensions.tools()

    def _read_tb_config(self, toolbelt_root):
        tb_config = self.file_wrapper.json_load(
                toolbelt_root + "/" + self.CONFIG_FILE)

        try:
            private_config = self.file_wrapper.json_load(
                    toolbelt_root + "/" + self.PRIVATE_CONFIG_FILE)

            tb_config.update(private_config)
        except IOError:
            pass

        return tb_config
