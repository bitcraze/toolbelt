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

from toolbelt.utils.exception import ToolbeltException

__author__ = 'kristoffer'


class BcModule:

    MODULE_CONFIG_FILE = 'module.json'
    MODULE_TOOL_PATH = 'tools'

    def __init__(self, docker, runner, file_wrapper):
        self.docker = docker
        self.runner = runner
        self.file_wrapper = file_wrapper

    def read_config(self, module_root):
        try:
            module_config = self.file_wrapper.json_load(
                    module_root + "/" + self.MODULE_CONFIG_FILE)

            version = self.verify_config_version(module_config)
            self.convert_old_config(version, module_config)
            return module_config
        except IOError:
            raise ToolbeltException("Could not find module configuration. Are "
                                    "you sure you are located in a module?")

    def execute_tool(self, tb_config, command, arguments):
        dir = tb_config['module_tools'][command]
        script = self.MODULE_TOOL_PATH + "/" + dir + '/' + command
        self.runner.run_script_in_env(tb_config, script,
                                      tb_config['module_root_in_docker_host'],
                                      arguments)

    def enumerate_tools(self, module_root, module_config):
        dirs = module_config["environmentReqs"].keys()
        result = {}
        for dir in dirs:
            try:
                tools_in_dir = os.listdir(module_root + "/" + self.MODULE_TOOL_PATH + "/" + dir)
                for tool in tools_in_dir:
                    if tool in result:
                        raise ToolbeltException("Tool '" + tool + "' exists in multiple directories, aborting.")
                    result[tool] = dir
            except OSError:
                pass
        return result

    def convert_old_config(self, version, config):
        if version == '1.0':
            config['environmentReqs'] = {"build": config["environmentReq"]}
            config.pop("environmentReq", None)

    def verify_config_version(self, config):
        config_version = "NA"
        if 'version' in config:
            config_version = config['version']

        if config_version != "1.0" and config_version != "2.0":
            raise ToolbeltException("module config version " + config_version +
                                    " not supported")

        return config_version
