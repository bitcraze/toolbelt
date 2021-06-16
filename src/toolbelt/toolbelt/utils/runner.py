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


class Runner:

    def __init__(self, docker):
        self.docker = docker

    def run_script_in_env(self, tb_config, script, module_root_in_docker_host, script_args):

        module_config = tb_config['module_config']
        dir = self._find_dir_for_script(module_config, script)
        image_name = self._find_image_for_environment(module_config, dir, tb_config)
        self._print_info(image_name, script, tb_config)

        # Try to get the latest builder image
        self.docker.pull_no_fail(image_name)

        self.docker.run_script_in_container(
            tb_config['uid'],
            image_name, script, script_args,
            volumes=[(module_root_in_docker_host, '/module')])

    def run_build_script_in_env(self, tb_config, module_config,
                                module_root_in_docker_host, script_args):
        script = "tools/build/build"
        if "buildScript" in module_config:
            script = module_config["buildScript"]

        image_name = self._find_image_for_environment(module_config, 'build', tb_config)
        self._print_info(image_name, script, tb_config)

        # Try to get the latest builder image
        self.docker.pull_no_fail(image_name)

        self.docker.run_script_in_container(
            tb_config['uid'], image_name, script, script_args,
            volumes_from=[tb_config['container_id']])

    def _find_dir_for_script(self, module_config, script):
        # Expect script to be something like "tools/build/the-tool"
        parts = script.split('/')
        if len(parts) != 3:
            raise ToolbeltException('Invalid script path: ' + script)
        return parts[1]

    def _find_image_for_environment(self, module_config, dir, tb_config):
        environment_requirements = module_config['environmentReqs'][dir]
        environments = tb_config['environments']
        requirements = set(environment_requirements)
        for image_name, properties in environments.items():
            if len(set(properties) & requirements) == len(requirements):
                return image_name
        raise ToolbeltException("Did not find a matching environment for the "
                                "requirements [" + ", ".join(requirements) +
                                "]")

    def _print_info(self, image_name, script, tb_config):
        user = "user root"
        uid = tb_config['uid']
        if uid != "0":
            user = "uid " + uid

        print("Running script " + script +
              " in a container based on the " + image_name +
              " docker image as " + user)
