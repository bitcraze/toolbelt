# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
# Toolbelt - a utility tu run tools in docker containers
# Copyright (C) 2019  Bitcraze AB
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


class Docs:
    def __init__(self, docker):
        self._docker = docker
        self._IMAGE = "bitcraze/web-builder"

    names = ['docs']
    short_description = "Serve docs locally"

    def command(self, tb_config, arguments):
        try:
            if len(arguments) > 1:
                raise ToolbeltException("Too many arguments")

            port = 80
            if len(arguments) == 1:
                port = int(arguments[0])

            self._pull_latest_image()
            self._run_jekyll(tb_config, port)
        except ValueError:
            raise ToolbeltException("Port must be integer number")

    def help(self):
        print("Usage:  tb docs [port]")
        print("Start a local web server and serve the documentation in the"
              "docs folder of a repository. Use when writing documentation to "
              "render a basic version of the documentation")

    def _pull_latest_image(self):
        self._docker.pull_no_fail(self._IMAGE)

    def _run_jekyll(self, tb_config, port):
        uid = tb_config['uid']

        args = ['jekyll', 'serve', '--host', '0.0.0.0', '--incremental',
                '--config', '/docs-config.yml', '--port', str(port)]
        volumes = [
            (tb_config['module_root_in_docker_host'] + '/docs', '/module/docs')
        ]
        ports = [(str(port), str(port))]

        print()
        print("Starting jekyll, serving on http://localhost:{}/docs".
              format(str(port)))
        print()
        self._docker.run_in_container(uid, self._IMAGE, args, volumes,
                                      ports=ports)
