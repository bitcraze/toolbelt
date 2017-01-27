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

import sys

from toolbelt.utils import exception
from toolbelt.utils.bc_module import BcModule
from toolbelt.utils.config_reader import ConfigReader
from toolbelt.utils.extensions import Extensions


class Toolbelt:
    def __init__(self, bc_module=BcModule(), config_reader=ConfigReader(),
                 extensions=Extensions()):
        self.bc_module = bc_module
        self.config_reader = config_reader
        self.extensions = extensions

    def _find_tool(self, tools, name):
        result = None

        for tool in tools:
            if name in tool.names:
                result = tool
                break

        return result

    def _main_raises(self, toolbelt_root):
        tb_config = self.config_reader.get_tb_config(
            toolbelt_root, self.extensions)

        if not tb_config['config_ok']:
            print("\033[91mWarning: It seems as your alias is not "
                  "set up correctly. Try to run with help\033[0m")

        command = 'help'
        if len(sys.argv) > 1:
            command = sys.argv[1]
        arguments = sys.argv[2:]

        self.extensions.pre_tool_execution(tb_config, command, arguments)

        tool = self._find_tool(tb_config['tools'], command)
        if tool is not None:
            tool.command(tb_config, arguments)
        elif command in tb_config['module_tools']:
            self.bc_module.execute_tool(tb_config, command, arguments)
        else:
            raise exception.ToolbeltException(
                    "Don't know how to execute " + command)

    def main(self, toolbelt_root):
        try:
            self._main_raises(toolbelt_root)
        except exception.ToolbeltException as e:
            print("\033[91mError: " + e.value + "\033[0m")
            sys.exit(-1)
