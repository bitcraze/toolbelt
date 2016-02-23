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
import os

from toolbelt.utils.exception import ToolbeltException
from toolbelt.utils.docker import Docker
from toolbelt.utils.file_wrapper import FileWrapper
from toolbelt.utils.runner import Runner

__author__ = 'kristoffer'


class BcModule:

    MODULE_CONFIG_FILE = 'module.json'
    MODULE_TOOL_PATH = 'tools/build'

    def __init__(self, docker=Docker(), runner=Runner(),
                 file_wrapper=FileWrapper()):
        self.docker = docker
        self.runner = runner
        self.file_wrapper = file_wrapper

    def read_config(self, module_root):
        try:
            module_config = self.file_wrapper.json_load(
                    module_root + "/" + self.MODULE_CONFIG_FILE)

            self.verify_config_version(module_config)
            return module_config
        except IOError as e:
            raise ToolbeltException("Could not find module configuration. Are "
                                    "you sure you are located in a module?")

    def execute_tool(self, tb_config, command, arguments):
        module_config = self.read_config(tb_config['module_root'])
        script = self.MODULE_TOOL_PATH + "/" + command
        self.runner.run_script_in_env(tb_config, module_config, script,
                                      tb_config['module_root_in_docker_host'],
                                      arguments)

    def enumerate_tools(self, module_root):
        try:
            return os.listdir(module_root + "/" + self.MODULE_TOOL_PATH)
        except OSError:
            return []

    def verify_config_version(self, config):
        config_version = "NA"
        if 'version' in config:
            config_version = config['version']

        if config_version != "1.0":
            raise ToolbeltException("module config version " + config_version +
                                    " not supported")
