#!/usr/bin/env python

"""
Creates a dummy Portal with some peers offering services.
A single user is always logged, in a real portal,
users should log-in.
"""

from intercoop import portalexample
from intercoop import peerinfo
from intercoop import userinfo
from intercoop import fixtures
from intercoop.fixtures import write

write('instance/somillusio/users/myuser.yaml', fixtures.myuseryaml)
write('instance/somillusio/peers/somenergia.yaml', fixtures.somenergiayaml)
write('instance/somillusio/peers/mesopcions.yaml', fixtures.mesopcionsyaml)
write('instance/somillusio/peers/sombogus.yaml', fixtures.sombogusyaml)
write('instance/somillusio/peers/somacme.yaml', fixtures.somacmeyaml)

p = portalexample.Portal(
    'intercoop',
    peerid='somillusio',
    keyfile='testkey.pem',
    peers = peerinfo.PeerInfo(
        'instance/somillusio/peers'),
    users = userinfo.UserInfo(
        'instance/somillusio/users'),
    )

p.run(
    debug=True,
    host='0.0.0.0',
    )

# vim: ts=4 sw=4 et
