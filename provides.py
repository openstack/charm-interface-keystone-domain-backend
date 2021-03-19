# Copyright 2017 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import uuid

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes

import charmhelpers.core.hookenv as hookenv


class KeystoneDomainBackendProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:keystone-domain-backend}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:keystone-domain-backend}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')

    def domain_name(self, name):
        """
        Set the domain name for the identity backend
        """
        relation_info = {
            'domain-name': name,
        }
        self.set_remote(**relation_info)

    def trigger_restart(self):
        """
        Trigger a restart of keystone
        """
        relation_info = {
            'restart-nonce': str(uuid.uuid4())
        }
        self.set_remote(**relation_info)

    def publish_releases_packages_map(self, releases_packages_map):
        """Publish releases_packages_map.

        :param releases_packages_map: Map of releases and packages
        :type releases_packages_map: Dict[str,Dict[str,List[str]]]
        """
        # NOTE: To allow relation updates outside of relation hook execution,
        # e.g. upgrade-charm hook, we need to revert to classic hookenv tools.
        for rid in hookenv.relation_ids(self.relation_name):
            relation_info = {
                'releases-packages-map': json.dumps(
                    releases_packages_map, sort_keys=True)
            }
            hookenv.relation_set(rid, relation_info)
