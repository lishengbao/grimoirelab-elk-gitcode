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

from grimoire_elk.raw.elastic import ElasticOcean
from grimoire_elk.elastic_mapping import Mapping as BaseMapping
from ..identities.gitcode import GitCodeIdentities


class Mapping(BaseMapping):

    @staticmethod
    def get_elastic_mappings(es_major):
        """Get Elasticsearch mapping.
        :param es_major: major version of Elasticsearch, as string
        :returns:        dictionary with a key, 'items', with the mapping
        """

        mapping = '''
         {
            "dynamic":true,
                "properties": {
                    "data": {
                        "dynamic":false,
                        "properties": {}
                    }
                }
        }
        '''

        return {"items": mapping}


class GitCodeOcean(ElasticOcean):
    """GitCode Ocean feeder"""

    mapping = Mapping
    identities = GitCodeIdentities

    @classmethod
    def get_perceval_params_from_url(cls, url):
        """ Get the perceval params given a URL for the data source """

        params = []

        tokens = url.split(' ', 1)  # Just split the URL not the filter
        url = tokens[0]

        owner = url.split('/')[-2]
        repository = url.split('/')[-1]
        params.append(owner)
        params.append(repository)
        return params

    def _fix_item(self, item):
        category = item['category']

        if 'classified_fields_filtered' not in item or not item['classified_fields_filtered']:
            return

        item = item['data']
        comments_attr = None
        if category == "issue":
            identity_types = ['user', 'assignee']
            comments_attr = 'comments_data'
        elif category == "pull_request":
            identity_types = ['user', 'merged_by']
            comments_attr = 'review_comments_data'
        else:
            identity_types = []

        for identity in identity_types:
            if identity not in item:
                continue
            if not item[identity]:
                continue

            identity_attr = identity + "_data"

            item[identity_attr] = {
                'name': item[identity]['login'],
                'login': item[identity]['login'],
                'email': None,
                'company': None,
                'location': None,
            }

        comments = item.get(comments_attr, [])
        for comment in comments:
            comment['user_data'] = {
                'name': comment['user']['login'],
                'login': comment['user']['login'],
                'email': None,
                'company': None,
                'location': None,
            }
