#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from intercoop import apiexample
from intercoop import remoteuserinfo
from intercoop import crypto
from intercoop import keyring
from intercoop import peerinfo
from intercoop import fixtures
from intercoop.fixtures import write, mkdir

import os

mkdir('instance/somacme/remoteusers')
write('instance/somacme/peers/somillusio.yaml', fixtures.somillusioyaml)
write('instance/somacme/peers/somenergia.yaml', fixtures.somenergiayaml)
write('instance/somacme/peers/mesopcions.yaml', fixtures.mesopcionsyaml)
write('instance/somacme/peers/sombogus.yaml', fixtures.sombogusyaml)
write('instance/somacme/peers/somacme.yaml', fixtures.somacmeyaml)

p = apiexample.IntercoopApi(
    'somacme',
    storage = remoteuserinfo.RemoteUserInfo('instance/somacme/remoteusers'),
    keyring = keyring.KeyRing(peers = peerinfo.PeerInfo('instance/somacme/peers')),
    continuationUrlTmpl = 'http://localhost:5001/continuation/{uuid}'
    )

p.run(
    debug=True,
    host='0.0.0.0',
    port=5001,
    )

# vim: ts=4 sw=4 et
