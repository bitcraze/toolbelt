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


class Help:
    names = ['help', '-h', '--help']
    short_description = "Help"

    def __init__(self):
        pass

    def command(self, tb_config, arguments):
        if len(arguments) == 0:
            self._general_help(tb_config)
        elif len(arguments) == 1:
            self._command_help(tb_config, arguments[0])
        else:
            print("Error: Use ony one argument for help")
            self._general_help(tb_config)

    def help(self):
        print("Usage:  tb help [tool]")
        print("Get help. Use with a tool to get help for that tool.")

    def _general_help(self, tb_config):
        print("Usage:  tb [-d] tool [arguments]")
        print("The toolbelt is used to develop, test and build Bitcraze "
              "modules. When the toolbelt is called, it will "
              "first try to find the tool in the belt, after that it will "
              "try the tools in the module if the working directory is the "
              "root of a module. Module tools are executed in the "
              "context of a docker container based on the module "
              "requirements configured in the module.json config file.")
        print("")
        print("-d:  print the docker call that executes the tool")
        print("")
        print('Tools in the belt:')
        for tool in tb_config["tools"]:
            print("  " + ", ".join(tool.names) + " - " +
                  tool.short_description)

        print("")
        if len(tb_config['module_tools']) > 0:
            print('Tools in the current module:')
            for tool in tb_config['module_tools'].keys():
                print("  " + tool)
        else:
            print("No tools found in the current module")

        if not tb_config['config_ok']:
            print("")
            print("Installation on linux, OSX and Windows:")
            print('Add "' + self._alias() + '" to your .profile or .bashrc')

    def _command_help(self, tb_config, command):
        for tool in tb_config["tools"]:
            if command in tool.names:
                tool.help()
                return
        print("No help for " + command)

    def _alias(self):
        return 'alias tb=\'docker run --rm -it -e \"HOST_CW_DIR=${PWD}\" ' \
               '-e "CALLING_HOST_NAME=$(hostname)" -e "CALLING_UID"=$UID -e ' \
               '"CALLING_OS"=$(uname) ' \
               '-v ${PWD}:/tb-module ' \
               '-v /var/run/docker.sock:/var/run/docker.sock ' \
               'bitcraze/toolbelt\''
