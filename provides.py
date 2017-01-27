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

import uuid

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


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
