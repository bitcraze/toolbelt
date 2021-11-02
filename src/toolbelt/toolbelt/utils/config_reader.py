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

__author__ = 'kristoffer'


class ConfigReader:
    CONFIG_FILE = 'config.json'
    PRIVATE_CONFIG_FILE = '.toolbelt.json'

    def __init__(self, file_wrapper, bc_module, tools):
        self.file_wrapper = file_wrapper
        self.bc_module = bc_module
        self.tools = tools

    def get_tb_config(self, toolbelt_root, extensions):
        tb_config = self._read_tb_config(toolbelt_root)

        tb_config['config_ok'] = True

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

        if "HOST_CW_DIR" in os.environ:
            tb_config['module_root_in_docker_host'] = os.environ["HOST_CW_DIR"]
            tb_config['container_id'] = os.environ["HOSTNAME"]

        tb_config["os"] = self._read_os(tb_config)
        tb_config["uid"] = self._read_uid(tb_config)

        if tb_config['config_ok']:
            tb_config['module_config'] = self.bc_module.read_config(tb_config['module_root'])
            tb_config['module_tools'] = self.bc_module.enumerate_tools(
                tb_config['module_root'], tb_config['module_config'])
        else:
            tb_config['module_tools'] = {}

        return tb_config

    def _read_os(self, tb_config):
        return self._read_with_fallback(
            "CALLING_OS", 'unknown', tb_config).lower()

    def _read_uid(self, tb_config):
        root_uid = "0"
        os = tb_config["os"]
        if os == 'linux':
            return self._read_with_fallback("CALLING_UID", root_uid, tb_config)
        return root_uid

    def _read_with_fallback(self, key, default, tb_config):
        if key in os.environ:
            value = os.environ[key]
            if len(value) > 0 and not value.isspace():
                return value
        tb_config['config_ok'] = False
        return default

    def _register_tools(self, extensions):
        return self.tools + extensions.tools()

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
