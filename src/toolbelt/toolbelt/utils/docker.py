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
import sys
import re
import subprocess

from toolbelt.utils import exception

__author__ = 'kristoffer'


class Docker:
    def __init__(self, sub_proc):
        self._sub_proc = sub_proc
        self.db_restart_wait_time = 1
        self.verbose = False

    def container_exist(self, container_name):
        result = self._sub_proc.call(
            ["docker", "inspect", "--format={{.Id}}", container_name],
            stdout=self._sub_proc.devnull,
            stderr=subprocess.STDOUT)
        return (result == 0)

    def stop_and_remove_container(self, container_name):
        self._sub_proc.check_call(["docker", "stop", container_name],
                                  stdout=self._sub_proc.devnull)
        self._sub_proc.check_call(["docker", "rm", "-v", container_name],
                                  stdout=self._sub_proc.devnull)

    def push(self, image_name):
        self._sub_proc.check_call(["docker", "push", image_name])

    def image_exists(self, image_name):
        try:
            self._sub_proc.check_output(["docker", "pull", image_name],
                                        stderr=subprocess.STDOUT)
            return True
        except exception.ToolbeltException as e:
            # TODO This is pretty brittle, improve! We parse the error text
            #  to determine if the image was not found or if the registry could
            #  not be contacted. Possible solution would be to use the API
            #  instead.
            if re.search(' not found', e.value):
                return False
            raise exception.ToolbeltException("Can not contact registry. " +
                                              e.value)

    def run_in_container(self, uid, image_name, args, volumes=[],
                         volumes_from=[], ports=[]):
        params = ['docker', 'run', '--rm', '-u', uid, '-v',
                  '/var/run/docker.sock:/var/run/docker.sock']

        if sys.stdout.isatty():
            params.append('-it')

        for volume in volumes:
            params.append('-v')
            params.append(volume[0] + ':' + volume[1])

        for volume in volumes_from:
            params.append('--volumes-from')
            params.append(volume)

        for port in ports:
            params.append('-p')
            params.append(port[0] + ':' + port[1])

        params.append(image_name)

        for arg in args:
            params.append(arg)

        if self.verbose:
            print('Running: ' + ' '.join(params))

        self._sub_proc.check_call(params)

    def run_script_in_container(self, uid, image_name, script, script_args,
                                volumes=[], volumes_from=[]):

        args = [script]
        for script_arg in script_args:
            args.append(script_arg)

        self.run_in_container(uid, image_name, args, volumes, volumes_from)

    def list_images(self):
        out = self._sub_proc.check_output(['docker', 'images'])
        lines = out.splitlines()[1:]
        return list(map(self._split_image_line, lines))

    def remove_images(self, ids):
        params = ["docker", "rmi"]
        for id in ids:
            params.append(id)

        self._sub_proc.check_call(params)

    def tag(self, existing_image, new_image):
        self._sub_proc.check_call(['docker', 'tag', existing_image, new_image])

    def pull(self, image):
        self._sub_proc.check_call(['docker', 'pull', image])

    def pull_no_fail(self, image):
        self._sub_proc.call(['docker', 'pull', image])

    def inspect(self, id):
        result = self._sub_proc.check_output(['docker', 'inspect', id])
        return json.loads(result)

    def list_volumes(self, filter=None):
        params = ['docker', 'volume', 'ls', '-q']
        if filter:
            params.append('-f')
            params.append(filter)
        out = self._sub_proc.check_output(params)
        return out.splitlines()

    def remove_volumes(self, ids):
        if ids:
            params = ["docker", "volume", "rm"]
            for id in ids:
                params.append(id)

            self._sub_proc.check_call(params)

    def _split_image_line(self, line):
        elements = line.split()
        return {"repo": elements[0], "tag": elements[1], "id": elements[2]}
