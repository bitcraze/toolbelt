# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
# Toolbelt - a utility tu run tools in docker containers
# Copyright (C) 2016-2018  Bitcraze AB
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
import urllib.request
from operator import itemgetter
from toolbelt.utils.exception import ToolbeltException

__author__ = 'kristoffer'


class Ghrn:
    names = ['ghrn']
    short_description = "Generate release notes from github milestone"

    def __init__(self, docker):
        self._docker = docker

    def command(self, tb_config, arguments):
        if len(arguments) != 2:
            raise ToolbeltException("Expecting 2 arguments")
        repo = arguments[0]
        milestone = arguments[1]
        self._display_release_notes(tb_config, repo, milestone)

    def help(self):
        print("Usage:  tb ghrn repository-url milestone")
        print("Generate release notes based on a milestone in a github ")
        print("repository. Extracts all issues from the mile stone and ")
        print("lists them.")
        print("")
        print("Example: tb ghrn bitcraze/crazyflie-firmware 2017.04")

    def _display_release_notes(self, tb_config, repo, milestone):
        all_milestones = self._api_get(
            "https://api.github.com/repos/" + repo + "/milestones?state=all")

        milestone_id = self._find_milestone_id(all_milestones, milestone)

        issues = self._api_get(
            "https://api.github.com/repos/" + repo + "/issues?milestone=" +
            str(milestone_id) + "&state=all")

        issues_list = self._collect_issues(issues)

        contributors = self._api_get(
            "https://api.github.com/repos/" + repo + "/contributors")
        contributor_list = self._collect_contributors(contributors)

        print("## Closed issues/pull requests")
        print('')
        print(issues_list)
        print('')
        print('## Contributors')
        print('')
        print(contributor_list)

    def _api_get(self, url):
        try:
            result = []
            current_url = url

            while current_url is not None:
                response = urllib.request.urlopen(current_url)
                body = response.read()
                result.extend(json.loads(str(body, 'utf-8')))
                link = response.getheader("Link")
                current_url = self._get_url_from_link(link)

            return result
        except urllib.error.HTTPError as e:
            raise ToolbeltException(
                "Failed to access github API for url {}. ({})".format(url, e))

    def _get_url_from_link(self, link):
        result = None

        if link is not None:
            parts = link.split(',')
            for part in parts:
                sub_parts = part.split(';')
                if sub_parts[1].strip() == 'rel="next"':
                    result = sub_parts[0].strip()[1:-1]

        return result

    def _find_milestone_id(self, all_milestones, milestone):
        for candidate in all_milestones:
            if candidate["title"] == milestone:
                return candidate["number"]
        raise ToolbeltException("Milestone " + milestone + " not found")

    def _collect_issues(self, issues):
        result = ""

        sorted_issues = sorted(issues, key=itemgetter('number'))
        for issue in sorted_issues:
            result = result + "#{} {}\n".format(issue["number"],
                                                issue["title"])

        return result

    def _collect_contributors(self, contributors):
        result = ""

        sorted_contributors = sorted(contributors, key=itemgetter('login'))

        for contributor in sorted_contributors:
            result = result + "{}\n".format(contributor["login"])

        return result
