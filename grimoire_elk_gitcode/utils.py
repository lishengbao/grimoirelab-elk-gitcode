# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Yehui Wang, Shengbao Li
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Yehui Wang <yehui.wang.mdh@gmail.com>
#   Shengbao Li <lishengbao147@gmail.com>

# Connectors for Perceval
from perceval.backends.gitcode.gitcode import GitCode, GitCodeCommand
# Connectors for EnrichOcean
from .enriched.gitcode import GitCodeEnrich
from .enriched.gitcode2 import GitCodeEnrich2
# Connectors for Ocean
from .raw.gitcode import GitCodeOcean


def get_connectors():

    return {"gitcode": [GitCode, GitCodeOcean, GitCodeEnrich, GitCodeCommand],
            "gitcode2": [GitCode, GitCodeOcean, GitCodeEnrich2, GitCodeCommand]}
