# Overview

This interface layer handles the communication with Keystone via the
'keystone-domain-backend' interface protocol.

# Usage

## Provides

The interface layer will set the following state:

  * `{relation_name}.connected`  The relation is established.

For example:

```python
from charms.reactive import when


@when('domain-backend.connected')
@when('configuration.complete')
def configure_domain(domain):
    domain.domain_name('mynewkeystonedomain')
    domain.trigger_restart()
```

Typically a domain backend charm should validate that that it
has sufficient and good configuration for the domain backend,
write its configuration to
`/etc/keystone/domains/keystone.<domain-name>.conf` and then
trigger a restart of keystone using the `trigger_restart`
method of the inteface, supplying the domain name at this
point in time as well.

The keystone charm will create the domain in the keystone
database, mapping to the underlying domain configuration
on disk.
