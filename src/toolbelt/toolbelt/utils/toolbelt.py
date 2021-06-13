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
from toolbelt.utils.docker import Docker
from toolbelt.utils.file_wrapper import FileWrapper
from toolbelt.utils.runner import Runner
from toolbelt.utils.subproc import SubProc
from toolbelt.utils.git import Git
from toolbelt.utils.ui import Ui
from toolbelt.belt import docs
from toolbelt.belt import help
from toolbelt.belt import update
from toolbelt.belt import version
from toolbelt.belt import ghrn


# Ultra Crude DI
class DependecyInjector:
    def __init__(self):
        self.sub_proc = SubProc()
        self.docker = Docker(self.sub_proc)
        self.runner = Runner(self.docker)
        self.file_wrapper = FileWrapper()
        self.bc_module = BcModule(self.docker, self.runner, self.file_wrapper)
        self.git = Git(self.sub_proc)
        self.ui = Ui()

        self.tools = [
            help.Help(),
            update.Update(self.docker),
            version.Version(self.docker),
            ghrn.Ghrn(self.docker),
            docs.Docs(self.docker),
        ]

        self.config_reader = ConfigReader(self.file_wrapper,
                                          self.bc_module,
                                          self.tools)


class Toolbelt:
    def __init__(self, bc_module, config_reader, docker, extensions):
        self.bc_module = bc_module
        self.config_reader = config_reader
        self.docker = docker
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

        verbose = False
        command = 'help'
        pos = 1

        if len(sys.argv) > pos:
            arg = sys.argv[pos]
            if arg == '-d':
                verbose = True
                pos += 1

        if len(sys.argv) > pos:
            command = sys.argv[pos]
            pos += 1

        arguments = sys.argv[pos:]

        self.docker.verbose = verbose
        self.extensions.pre_tool_execution(tb_config, command, arguments)

        tool = self._find_tool(tb_config['tools'], command)
        if tool is not None:
            tool.command(tb_config, arguments)
        elif command in tb_config['module_tools']:
            self.bc_module.execute_tool(tb_config, command, arguments)
        else:
            raise exception.ToolbeltException("Don't know how to execute " + command)

    def main(self, toolbelt_root):
        try:
            self._main_raises(toolbelt_root)
        except exception.ToolbeltException as e:
            print("\033[91mError: " + e.value + "\033[0m")
            sys.exit(-1)
